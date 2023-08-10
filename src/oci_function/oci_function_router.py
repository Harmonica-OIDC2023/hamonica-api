from fastapi import APIRouter, Response

from src.oci_function.dto.oci_function_dto import CreateFunctionDto, DeployFunctionDto
from src.oci_function.oci_function_services import OciFunctionServices

router = APIRouter(prefix="/api/v1/oci-functions", tags=["oci-functions"])


@router.post(path="/")
async def create_oci_function(create_function_dto: CreateFunctionDto):
    oci_functions_services = OciFunctionServices()
    oci_functions_services.create_function_in_oci(create_function_dto.function_name)
    return Response(status_code=200)


@router.post(path="/deploy")
async def deploy_oci_function(deploy_function_dto: DeployFunctionDto):
    oci_functions_services = OciFunctionServices()
    oci_functions_services.deploy_function_by_id(
        deploy_function_dto.fnapp_name, deploy_function_dto.function_name
    )
    return Response(status_code=200)


@router.get(path="/")
async def get_oci_function_by_id(fnapp_id: str):
    oci_functions_services = OciFunctionServices()
    return [oci_functions_services.get_function_by_id(fnapp_id)]


@router.post(path="/init")
async def get_oci_function_by_id(function_name: str):
    oci_functions_services = OciFunctionServices()
    return [oci_functions_services.init_function_by_function_name(function_name)]
