from __future__ import annotations

import gateway_oss.main as gateway_oss_main

app = gateway_oss_main.app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "gateway.main:app", host="0.0.0.0", port=5001, reload=True, loop="uvloop"
    )
