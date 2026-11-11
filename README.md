# PatchWise AI

AI Code Evaluation, Repository Repair, and Software Engineering Benchmark Platform.

## 🚀 Overview
PatchWise AI is an enterprise-grade full-stack platform designed to evaluate software engineering solutions. It allows authors to create coding challenges, and candidates to submit code patches that are securely executed and evaluated in isolated, network-disabled Docker sandboxes.

## 🛠️ Technology Stack
* **Backend:** Python, FastAPI, SQLAlchemy, Alembic
* **Workers:** Celery (Python), Redis (Pub/Sub)
* **Database:** PostgreSQL
* **Execution Engine:** Docker (Isolated Sandbox)
* **Frontend:** React, TypeScript, Monaco Editor, React Query, Recharts
* **Infrastructure:** Docker, Docker Compose

## ✨ Key Features
* Multi-Tenant Architecture: Complete organization and role-based isolation.
* Isolated Execution Engine: Candidate code is evaluated in a secure, memory-limited, network-disabled Docker container.
* Fail-to-Pass Testing: The engine verifies that the bug exists on the baseline and is fixed by the candidate's patch.
* Real-Time Monitoring: WebSockets and Redis Pub/Sub stream live execution logs directly to the React dashboard.
* Professional UI: Dark theme, live Recharts analytics, and a browser-based Monaco Editor (the engine behind VS Code).

## 🚦 Getting Started

### Prerequisites
* Docker Desktop installed and running.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Adijah6838/patchwise.git