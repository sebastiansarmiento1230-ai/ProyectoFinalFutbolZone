from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class NotificacionModel(Base):
    __tablename__ = "notificaciones"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo      = Column(String(200), nullable=False)
    mensaje     = Column(Text, nullable=False)
    tipo        = Column(String(50), default="reserva")   # reserva | sistema | promo | pago
    leida       = Column(Boolean, default=False)
    reserva_id  = Column(Integer, ForeignKey("reservas.id", ondelete="SET NULL"), nullable=True, index=True)
    creado_en   = Column(DateTime, server_default=func.now())

    # Relaciones
    usuario = relationship("UsuarioModel", back_populates="notificaciones")
    reserva = relationship("ReservaModel", back_populates="notificaciones")
