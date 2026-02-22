from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.v1 import router as v1_router
from client.exceptions import SubstackAPIError, SubstackAuthError

app = FastAPI(
    title="Substack Gateway",
    description="REST API gateway for Substack",
    version="1.0.0",
)


@app.exception_handler(SubstackAuthError)
async def substack_auth_error_handler(
    request: Request, exc: SubstackAuthError
) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(SubstackAPIError)
async def substack_api_error_handler(
    request: Request, exc: SubstackAPIError
) -> JSONResponse:
    # Map specific upstream codes to semantically correct HTTP responses;
    # everything else becomes 502 Bad Gateway.
    _PASSTHROUGH = {404, 429}
    status = exc.status_code if exc.status_code in _PASSTHROUGH else 502
    return JSONResponse(status_code=status, content={"detail": exc.message})


app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
