from pydantic import BaseModel


class CreateOciApplicationRequestDto(BaseModel):
    compartment_id: str
    fnapp_name: str
    subnet_id: str
    ords_base_url: str
    db_user_secret_ocid: str
    db_password_secret_ocid: str
