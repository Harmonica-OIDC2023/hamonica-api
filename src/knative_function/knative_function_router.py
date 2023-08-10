from fastapi import APIRouter, Response

from src.knative_function.dto.knative_function_dto import (
    CreateFunctionDto,
    CreateSecretDto,
    DeployFunctionDto,
)
from src.knative_function.knative_function_services import KnativeFunctionServices

router = APIRouter(prefix="/api/v1/knative-functions", tags=["knative-functions"])


@router.post(path="/")
async def create_knative_function(create_function_dto: CreateFunctionDto):
    knaitve_functions_services = KnativeFunctionServices()
    return knaitve_functions_services.create_function_in_knative(
        create_function_dto.function_name
    )


@router.post(path="/deploy")
async def deploy_knative_function(deploy_function_dto: DeployFunctionDto):
    knaitve_functions_services = KnativeFunctionServices()
    return knaitve_functions_services.deploy_function_in_knative(
        function_name=deploy_function_dto.function_name,
        tenancy_namespace=deploy_function_dto.tenancy_namespace,
    )


@router.post(path="/create-secret")
async def create_secret_in_knative(create_secret_dto: CreateSecretDto):
    knaitve_functions_services = KnativeFunctionServices()
    return knaitve_functions_services.create_secret_for_registry(
        user_email=create_secret_dto.user_email,
        tenancy_namespace=create_secret_dto.tenacy_namespace,
        user_password=create_secret_dto.user_password,
    )


@router.put(path="/service-account")
async def update_service_account_in_k8s():
    knaitve_functions_services = KnativeFunctionServices()
    knaitve_functions_services.k8s_update_with_service_account()
    return Response(200)
