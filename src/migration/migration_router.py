from typing import Annotated

from fastapi import APIRouter, File, Form, Response, UploadFile

from src.migration.migration_services import MigrationServices

router = APIRouter(prefix="/api/v1/migration", tags=["migration"])


@router.post(path="/knative-to-oci")
async def knative_to_oci(
    user: Annotated[str, Form()],
    fingerprint: Annotated[str, Form()],
    tenancy: Annotated[str, Form()],
    region: Annotated[str, Form()],
    subnet_id: Annotated[str, Form()],
    fnapp_name: Annotated[str, Form()],
    compartment_id: Annotated[str, Form()],
    apideploy_name: Annotated[str, Form()],
    apigw_name: Annotated[str, Form()],
    registry: Annotated[str, Form()],
    api_url: Annotated[str, Form()],
    docker_registry: Annotated[str, Form()],
    docker_pw: Annotated[str, Form()],
    user_email: Annotated[str, Form()],
    func_name: Annotated[str, Form()],
    requirements: Annotated[UploadFile, File()],
    func_file: Annotated[UploadFile, File()],
    key_pem: Annotated[UploadFile, File()],
):
    migration = MigrationServices()
    endpoint = migration.set_oci(
        user=user,
        fingerprint=fingerprint,
        tenancy=tenancy,
        region=region,
        subnet_id=subnet_id,
        fnapp_name=fnapp_name,
        compartment_id=compartment_id,
        api_gateway_name=apigw_name,
        registry=registry,
        api_url=api_url,
        api_gateway_deploy_name=apideploy_name,
        docker_registry=docker_registry,
        user_email=user_email,
        docker_pw=docker_pw,
        function_name=func_name,
        requirements=await requirements.read(),
        func_file=await func_file.read(),
        key_pem=await key_pem.read(),
    )
    return Response(status_code=200, content={"endpoint": endpoint})


@router.post(path="/oci-to-knative")
async def oci_to_knative(
    docker_registry: Annotated[str, Form()],
    docker_pw: Annotated[str, Form()],
    user_email: Annotated[str, Form()],
    func_name: Annotated[str, Form()],
    requirements: Annotated[UploadFile, File()],
    func_file: Annotated[UploadFile, File()],
):
    migration = MigrationServices()
    migration.set_knative(
        docker_registry=docker_registry,
        docker_pw=docker_pw,
        user_email=user_email,
        function_name=func_name,
        requirements=await requirements.read(),
        func_file=await func_file.read(),
    )
    return Response(200)
