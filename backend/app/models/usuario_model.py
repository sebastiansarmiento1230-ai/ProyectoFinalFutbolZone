from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from app.config.database import Base


class RolUsuario(str, enum.Enum):
    admin   = "admin"
    cliente = "cliente"


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid            = Column(String(36), unique=True, nullable=True, index=True, default=lambda: str(uuid.uuid4()))
    nombre          = Column(String(100), nullable=False)
    apellido        = Column(String(100), nullable=False)
    nombre_completo = Column(String(200), nullable=True)
    email           = Column(String(150), unique=True, nullable=False, index=True)
    telefono        = Column(String(20))
    password_hash   = Column(String(255), nullable=False)
    rol             = Column(Enum(RolUsuario), default=RolUsuario.cliente, nullable=False)
    activo          = Column(Boolean, default=True)

    # Campos de perfil deportivo del jugador
    username        = Column(String(50), nullable=True)
    posicion        = Column(String(50), default="Delantero")
    pie_habil       = Column(String(20), default="Derecho")
    dorsal          = Column(Integer, default=10)
    bio             = Column(String(255), nullable=True)
    avatar          = Column(String(255), nullable=True)

    creado_en       = Column(DateTime, server_default=func.now())
    actualizado_en  = Column(DateTime, onupdate=func.now())

    # Relaciones
    reservas         = relationship("ReservaModel",         back_populates="usuario", cascade="all, delete-orphan")
    pagos            = relationship("PagoModel",            back_populates="usuario")
    torneos_inscrito = relationship("InscripcionTorneoModel", back_populates="usuario")
    notificaciones   = relationship("NotificacionModel",    back_populates="usuario", cascade="all, delete-orphan")
