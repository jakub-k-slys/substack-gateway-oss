from __future__ import annotations

import os

from gateway_oss import create_app

app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(
        "substack_gateway.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5001")),
        loop="uvloop",
    )


if __name__ == "__main__":
    main()
