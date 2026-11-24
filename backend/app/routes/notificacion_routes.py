from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.utils.auth import get_usuario_actual
from app.controllers.notificacion_controller import (
    get_notificaciones_usuario,
    get_conteo_no_leidas,
    marcar_leida,
    marcar_todas_leidas,
)

router = APIRouter(prefix="/api/notificaciones", tags=["Notificaciones"])


@router.get("/")
def listar(
    solo_no_leidas: bool = False,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(get_usuario_actual),
):
    usuario_id = int(usuario_actual.get("sub", 0))
    return get_notificaciones_usuario(usuario_id, db, solo_no_leidas)


@router.get("/conteo")
def conteo(
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(get_usuario_actual),
):
    usuario_id = int(usuario_actual.get("sub", 0))
    return get_conteo_no_leidas(usuario_id, db)


@router.patch("/{id}/leer")
def leer_una(
    id: int,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(get_usuario_actual),
):
    usuario_id = int(usuario_actual.get("sub", 0))
    return marcar_leida(id, usuario_id, db)


@router.patch("/leer-todas")
def leer_todas(
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(get_usuario_actual),
):
    usuario_id = int(usuario_actual.get("sub", 0))
    return marcar_todas_leidas(usuario_id, db)
