import os

from fastapi import FastAPI

from dto.oci_cli_dto import OciCliVersionDto
from middleware.interceptor import SealAPIMiddleware

app = FastAPI()
app.add_middleware(SealAPIMiddleware)


@app.get("/")
def read_root():
    return {"Hello": "Harmonica"}


@app.get(path="/oci-cli-version")
async def get_oci_cli_version() -> OciCliVersionDto:
    return OciCliVersionDto(version=os.popen("oci --version").read().strip())
