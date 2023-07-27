from pydantic import BaseModel


class OciCliVersionDto(BaseModel):
    version: str
