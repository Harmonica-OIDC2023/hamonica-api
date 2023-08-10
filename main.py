import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dto.oci_cli_dto import OciCliVersionDto
from middleware.interceptor import SealAPIMiddleware
from src.knative_function.knative_function_router import (
    router as knative_function_router,
)
from src.migration.migration_router import router as migration_router
from src.oci_api_gateway.oci_api_gateway_router import router as oci_api_gateway_router
from src.oci_application.oci_application_router import router as oci_application_router
from src.oci_function.oci_function_router import router as oci_function_router
from src.script_converter.script_converter_router import (
    router as script_converter_router,
)

app = FastAPI()

app.include_router(oci_function_router)
app.include_router(oci_application_router)
app.include_router(oci_api_gateway_router)
app.include_router(script_converter_router)
app.include_router(knative_function_router)
app.include_router(migration_router)
app.add_middleware(SealAPIMiddleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "Harmonica"}


@app.get(path="/oci-cli-version")
async def get_oci_cli_version() -> OciCliVersionDto:
    return OciCliVersionDto(version=os.popen("oci --version").read().strip())
