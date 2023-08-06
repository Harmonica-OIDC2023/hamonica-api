from pydantic import BaseModel


class CreateApiGatewayDto(BaseModel):
    compartment_id: str
    subnet_id: str
    api_gateway_name: str
    endpoint_type: str  # PUBLIC


class GetApiGatewayDeploymentListDto(BaseModel):
    compartment_id: str
