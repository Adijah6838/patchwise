import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints.ws import listen_to_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the Redis subscriber in the background
    task = asyncio.create_task(listen_to_redis())
    yield
    task.cancel()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

# Include Routers
from app.api.v1.endpoints import auth, repositories, challenges, submissions, ws
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(repositories.router, prefix=f"{settings.API_V1_PREFIX}/repositories", tags=["Repositories"])
app.include_router(challenges.router, prefix=f"{settings.API_V1_PREFIX}/challenges", tags=["Challenges"])
app.include_router(submissions.router, prefix=f"{settings.API_V1_PREFIX}/submissions", tags=["Submissions"])
app.include_router(ws.router, prefix="/ws", tags=["WebSockets"])