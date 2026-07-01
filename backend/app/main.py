from fastapi import FastAPI, status
from app.routes.tasks import router as tasks_router

app = FastAPI(
    title="Learning Cloud",
    version="0.1.0",
)


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "learningcloud-api",
    }


app.include_router(tasks_router)