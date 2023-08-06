from fastapi import APIRouter

from src.oci_function.dto.oci_function_dto import DeployFunctionDto, GetFunctionListDto
from src.oci_function.oci_function_services import OciFunctionServices

router = APIRouter(prefix="/api/v1/oci-functions", tags=["oci-functions"])


@router.post(path="/")
async def create_oci_application(deploy_function_dto: DeployFunctionDto):
    oci_functions_services = OciFunctionServices()
    return [oci_functions_services.deploy_function(deploy_function_dto)]


@router.get(path="/")
async def get_oci_application_list(fnapp_id: str):
    oci_functions_services = OciFunctionServices()
    return [oci_functions_services.get_function_list(fnapp_id)]
