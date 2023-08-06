import typing

from fastapi import APIRouter, Response

from src.oci_application.dto.oci_application_request_dto import (
    CreateOciApplicationRequestDto,
)
from src.oci_application.oci_application_services import OciApplicationServices

router = APIRouter(prefix="/api/v1/oci-applications", tags=["oci-applications"])


@router.post(path="/")
async def create_oci_application(
    create_oci_application_dto: typing.Union[CreateOciApplicationRequestDto, dict],
):
    oci_application_services = OciApplicationServices()
    return oci_application_services.create_application(
        compartment_id=create_oci_application_dto.compartment_id,
        fnapp_name=create_oci_application_dto.fnapp_name,
        subnet_id=create_oci_application_dto.subnet_id,
        ords_base_url=create_oci_application_dto.ords_base_url,
        db_user_secret_ocid=create_oci_application_dto.db_user_secret_ocid,
        db_password_secret_ocid=create_oci_application_dto.db_password_secret_ocid,
    )


@router.get(path="/")
async def get_oci_application_list(compartment_id: str):
    oci_application_services = OciApplicationServices()
    return oci_application_services.get_application_list(compartment_id)
