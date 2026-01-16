from fastapi import FastAPI, Request
from datetime import datetime
import socket

app = FastAPI()
# https://stannic-deservedly-lucca.ngrok-free.dev

@app.get("/health")
async def healthcheck(request: Request):
    return {
        "status": "OK",
        "service": "local-rcs",
        "hostname": socket.gethostname(),
        "client_ip": request.client.host if request.client else None,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
