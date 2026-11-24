from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UsuarioSchema(BaseModel):
    nombre:   str
    apellido: str
    correo:   EmailStr
    password: str
    telefono: Optional[str] = None

    @field_validator("nombre", "apellido")
    @classmethod
    def no_vacio(cls, v: str) -> str:
        limpio = v.strip()
        if not limpio:
            raise ValueError("El campo no puede estar vacío")
        return limpio

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if not v or len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v


class UsuarioLoginSchema(BaseModel):
    correo:   EmailStr
    password: str


class UsuarioUpdateSchema(BaseModel):
    nombre:   Optional[str]  = None
    apellido: Optional[str]  = None
    telefono: Optional[str]  = None
    activo:   Optional[bool] = None


class UsuarioOutSchema(BaseModel):
    id:              int
    uuid:            Optional[str] = None
    nombre:          str
    apellido:        str
    nombre_completo: Optional[str] = None
    correo:          str
    telefono:        Optional[str]
    rol:             str
    activo:          bool
    creado_en:       Optional[datetime]

    model_config = {"from_attributes": True}
