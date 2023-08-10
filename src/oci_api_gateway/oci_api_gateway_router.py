from fastapi import APIRouter

from src.oci_api_gateway.dto.oci_api_gateway_dto import CreateApiGatewayDto
from src.oci_api_gateway.oci_api_gateway_services import OciApiGatewayServices

router = APIRouter(prefix="/api/v1/oci-api-gateways", tags=["oci-api-gateways"])


@router.post(path="/")
async def create_api_gateway(create_api_gateway_dto: CreateApiGatewayDto):
    oci_api_gateway_services = OciApiGatewayServices()
    return [
        oci_api_gateway_services.create_api_gateway(
            compartment_id=create_api_gateway_dto.compartment_id,
            endpoint_type=create_api_gateway_dto.endpoint_type,
            subnet_id=create_api_gateway_dto.subnet_id,
            api_gateway_name=create_api_gateway_dto.api_gateway_name,
        )
    ]


@router.get(path="/deployment-list")
async def get_api_gateway_deployment_list(compartment_id: str,):
    oci_api_gateway_services = OciApiGatewayServices()
    return [oci_api_gateway_services.get_api_gateway_deployment_list(compartment_id)]
