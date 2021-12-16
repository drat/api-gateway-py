import sys
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import Database
from app.methods.core import Core

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8060"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/{version}/{service}/{endpoint}/{func_sn}")
async def apiGateway(
    version:str,
    service:str,
    endpoint:str,
    func_sn:str,
    payload:dict,
    q: Optional[str] = None
):
    connect = Database.mysql()
    cursor = connect.cursor(dictionary=True)
    result = Core.uagw(cursor, version, service, endpoint, func_sn, payload, q)
    connect.close()

    return {"response": result}


@app.get("/")
async def getDefaultMessage():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    message = f"FastAPI running currently on Uvicorn with Gunicorn. Using python v-{version}"

    return {"response": message}


if __name__ == "__main__":
    app.run(debug=True)

