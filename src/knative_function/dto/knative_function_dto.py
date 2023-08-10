from pydantic import BaseModel


class CreateFunctionDto(BaseModel):
    function_name: str


class DeployFunctionDto(BaseModel):
    function_name: str
    tenancy_namespace: str


class CreateSecretDto(BaseModel):
    user_email: str
    tenacy_namespace: str
    user_password: str
