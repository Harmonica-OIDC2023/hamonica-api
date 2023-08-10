from pydantic import BaseModel


class DeployFunctionDto(BaseModel):
    fnapp_name: str
    function_name: str


class GetFunctionListDto(BaseModel):
    fnapp_id: str


class CreateFunctionDto(BaseModel):
    function_name: str
