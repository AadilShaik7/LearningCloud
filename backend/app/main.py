from fastapi import FastAPI

app = FastAPI(
    title = "Learning Cloud",
    version = "0.1.0",
)

@app.get("/health")
def health_check():
    return {
        "status" : "ok",
        "service" : "learningcloud-api"
    }