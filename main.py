from fastapi import FastAPI

from api.v1 import router as v1_router

app = FastAPI(
    title="Substack Gateway",
    description="REST API gateway for Substack",
    version="1.0.0",
)

app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
