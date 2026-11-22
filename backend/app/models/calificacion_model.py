from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class CalificacionJugadorModel(Base):
    __tablename__ = "calificaciones_jugador"

    id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    evaluador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    jugador_id   = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estrellas    = Column(Integer, nullable=False, default=5)  # 1 a 5
    comentario   = Column(Text, nullable=True)
    creado_en    = Column(DateTime, server_default=func.now())

    # Relaciones
    evaluador = relationship("UsuarioModel", foreign_keys=[evaluador_id])
    jugador   = relationship("UsuarioModel", foreign_keys=[jugador_id])

    __table_args__ = (
        UniqueConstraint("evaluador_id", "jugador_id", name="uq_evaluador_jugador"),
    )


class CalificacionServicioModel(Base):
    __tablename__ = "calificaciones_servicio"

    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reserva_id    = Column(Integer, ForeignKey("reservas.id"), unique=True, nullable=False)
    usuario_id    = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cancha_id     = Column(Integer, ForeignKey("canchas.id"), nullable=False)
    atencion      = Column(Integer, nullable=False, default=5)  # 1 a 5
    servicio      = Column(Integer, nullable=False, default=5)  # 1 a 5
    instalaciones = Column(Integer, nullable=False, default=5)  # 1 a 5
    experiencia   = Column(Integer, nullable=False, default=5)  # 1 a 5
    promedio      = Column(Float, nullable=False, default=5.0)
    comentario    = Column(Text, nullable=True)
    creado_en     = Column(DateTime, server_default=func.now())

    # Relaciones
    reserva = relationship("ReservaModel")
    usuario = relationship("UsuarioModel")
    cancha  = relationship("CanchaModel")
