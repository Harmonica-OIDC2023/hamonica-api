from fastapi import APIRouter

from src.script_converter.dto.script_converter_dto import ScriptConverterRequestDto
from src.script_converter.script_converter_services import ScriptConverterServices

router = APIRouter(prefix="/api/v1/script-converter", tags=["script-converter"])


@router.post(path="/oci-to-knative")
async def oracle_cloud_infrastructure_to_knative(
    python_script_dto: ScriptConverterRequestDto,
):
    script_converter_services = ScriptConverterServices()
    return script_converter_services.get_oci_python_code_by_knative_python_code(
        python_script_dto.python_code
    )


@router.post(path="/knative-to-oci")
async def knative_to_oracle_cloud_infrastructure(
    python_script_dto: ScriptConverterRequestDto,
):
    script_converter_services = ScriptConverterServices()
    return script_converter_services.get_oci_python_code_by_knative_python_code(
        python_script_dto.python_code
    )
