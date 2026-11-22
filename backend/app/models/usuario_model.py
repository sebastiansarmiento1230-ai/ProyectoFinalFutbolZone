from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.config.database import Base


class RolUsuario(str, enum.Enum):
    admin   = "admin"
    cliente = "cliente"


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id             = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre         = Column(String(100), nullable=False)
    apellido       = Column(String(100), nullable=False)
    email          = Column(String(150), unique=True, nullable=False, index=True)
    telefono       = Column(String(20))
    password_hash  = Column(String(255), nullable=False)
    rol            = Column(Enum(RolUsuario), default=RolUsuario.cliente)
    activo         = Column(Boolean, default=True)

    # Campos de perfil deportivo del jugador
    username       = Column(String(50), nullable=True)
    posicion       = Column(String(50), default="Delantero")
    pie_habil      = Column(String(20), default="Derecho")
    dorsal         = Column(Integer, default=10)
    bio            = Column(String(255), nullable=True)
    avatar         = Column(String(255), nullable=True)

    creado_en      = Column(DateTime, server_default=func.now())
    actualizado_en = Column(DateTime, onupdate=func.now())

    # Relaciones
    reservas         = relationship("ReservaModel",         back_populates="usuario")
    pagos            = relationship("PagoModel",            back_populates="usuario")
    torneos_inscrito = relationship("InscripcionTorneoModel", back_populates="usuario")
