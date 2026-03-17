from __future__ import annotations

from gateway.app_factory import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "gateway.main:app", host="0.0.0.0", port=5001, reload=True, loop="uvloop"
    )
