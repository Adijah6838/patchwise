import docker
import os
import shutil
import random
import string

class ExecutionEngine:
    def __init__(self):
        self.client = docker.from_env()
        self.image = "patchwise-python-eval:latest"

    def _run_sandbox(self, host_temp_dir, test_command):
        """Helper method to spin up the Docker container and run a command."""
        container = None
        try:
            container = self.client.containers.run(
                image=self.image,
                # Add -p no:cacheprovider to stop pytest from trying to write cache files
                command=f"{test_command} -p no:cacheprovider", 
                volumes={host_temp_dir: {'bind': '/app', 'mode': 'rw'}},
                working_dir='/app',
                network_mode='none', 
                mem_limit='256m',    
                user='1000:1000',    
                detach=True
            )
            
            result = container.wait()
            exit_code = result.get('StatusCode', 1)
            logs_bytes = container.logs(stdout=True, stderr=True)
            logs = logs_bytes.decode("utf-8") if logs_bytes else ""
            
            return exit_code, logs
        finally:
            if container is not None:
                try: container.remove(force=True)
                except: pass

    def run_evaluation(self, repo_path: str, code_patch: str, language: str, test_command: str = "pytest"):
        host_project_path = os.environ.get("HOST_PROJECT_PATH", "").replace("\\", "/")
        if not host_project_path:
            return {"status": "error", "logs": "HOST_PROJECT_PATH environment variable is not set"}
        
        temp_dir_name = "temp_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        container_temp_dir = f"/app/sample-repositories/{temp_dir_name}"
        host_temp_dir = f"{host_project_path}/sample-repositories/{temp_dir_name}"
        
        os.makedirs(container_temp_dir, exist_ok=True)
        
        try:
            # 1. Copy the repository files into the temp directory
            source_dir = os.path.abspath(repo_path)
            for item in os.listdir(source_dir):
                if item == temp_dir_name: continue
                s = os.path.join(source_dir, item)
                d = os.path.join(container_temp_dir, item)
                if os.path.isdir(s): shutil.copytree(s, d)
                else: shutil.copy2(s, d)

            # ==========================================
            # PHASE 1: FAIL-TO-PASS (Baseline Test)
            # Run tests against the ORIGINAL buggy code
            # ==========================================
            baseline_exit_code, baseline_logs = self._run_sandbox(host_temp_dir, test_command)
            
            if baseline_exit_code == 0:
                return {
                    "status": "invalid_challenge", 
                    "logs": "Evaluation failed: The baseline tests PASSED against the original buggy code. The test suite does not correctly identify the defect."
                }

            # ==========================================
            # PHASE 2: CANDIDATE TEST (Apply Patch)
            # Overwrite the target file with the candidate's fix
            # ==========================================
            target_file = os.path.join(container_temp_dir, "calculator.py")
            with open(target_file, "w") as f:
                f.write(code_patch)

            candidate_exit_code, candidate_logs = self._run_sandbox(host_temp_dir, test_command)

            # ==========================================
            # PHASE 3: EVALUATE RESULTS
            # ==========================================
            if candidate_exit_code == 0:
                return {
                    "status": "passed", 
                    "logs": f"✅ Fix Verified!\n\nBaseline (Buggy): Failed as expected.\nCandidate (Patched): Passed!\n\n--- Candidate Test Output ---\n{candidate_logs}"
                }
            else:
                return {
                    "status": "failed", 
                    "logs": f"❌ Fix Failed. The candidate patch did not resolve the issue.\n\n--- Candidate Test Output ---\n{candidate_logs}"
                }

        except Exception as e:
            return {"status": "error", "logs": str(e)}
        finally:
            shutil.rmtree(container_temp_dir, ignore_errors=True)