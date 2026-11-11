import json
import redis
from app.workers.celery_app import celery_app
from app.database.session import SessionLocal
from app.models.submission import Submission
from app.models.challenge import Challenge
from app.execution.engine import ExecutionEngine
from app.core.config import settings

# Synchronous Redis client for Celery
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

@celery_app.task(name="evaluate_submission")
def evaluate_submission(submission_id: str):
    db = SessionLocal()
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        return {"error": "Submission not found"}

    challenge = db.query(Challenge).filter(Challenge.id == submission.challenge_id).first()
    
    # 1. Broadcast: Running
    submission.status = "running"
    db.commit()
    redis_client.publish("evaluation_events", json.dumps({
        "submission_id": str(submission.id), "status": "running", "message": "Spinning up sandbox..."
    }))
    
    print(f"🔬 [EVALUATION WORKER] Starting evaluation for submission: {submission_id}")
    
    engine = ExecutionEngine()
    repo_path = f"/app/sample-repositories/calculator" 
    test_command = challenge.evaluation_config.get("test_command", "pytest")

    result = engine.run_evaluation(
        repo_path=repo_path,
        code_patch=submission.code_patch,
        language=challenge.language,
        test_command=test_command
    )

    # 2. Broadcast: Completed
    submission.status = "completed"
    submission.test_results = {"result": result["status"]}
    submission.execution_logs = result["logs"]
    db.commit()
    db.close()

    redis_client.publish("evaluation_events", json.dumps({
        "submission_id": str(submission.id), 
        "status": result["status"],
        "message": "Evaluation complete!",
        "logs": result["logs"][:200] # Send a snippet of logs
    }))

    print(f"✅ [EVALUATION WORKER] Finished submission {submission_id}: {result['status']}")
    return result