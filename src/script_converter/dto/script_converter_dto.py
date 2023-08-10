from pydantic import BaseModel


class ScriptConverterRequestDto(BaseModel):
    python_code: str
