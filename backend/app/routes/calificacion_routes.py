from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.utils.auth import get_current_user, require_admin
from app.controllers.calificacion_controller import (
    calificar_jugador,
    get_calificaciones_jugador,
    calificar_servicio,
    get_calificaciones_servicio_admin
)

router = APIRouter(prefix="/api/calificaciones", tags=["Calificaciones"])


# ── CALIFICACIONES DE JUGADORES ──
@router.post("/jugador")
def post_calificar_jugador(
    body: dict,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user)
):
    return calificar_jugador(usuario_actual["sub"], body, db)


@router.get("/jugador/{jugador_id}")
def get_opiniones_jugador(
    jugador_id: int,
    db: Session = Depends(get_db)
):
    return get_calificaciones_jugador(jugador_id, db)


# ── CALIFICACIONES DEL SERVICIO (POST-RESERVA) ──
@router.post("/servicio")
def post_calificar_servicio(
    body: dict,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user)
):
    return calificar_servicio(usuario_actual["sub"], body, db)


@router.get("/servicio/admin")
def get_servicio_admin(
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    return get_calificaciones_servicio_admin(db)
