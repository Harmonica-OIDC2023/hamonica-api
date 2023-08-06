from pydantic import BaseModel


class DeployFunctionDto(BaseModel):
    fnapp_name: str


class GetFunctionListDto(BaseModel):
    fnapp_id: str
