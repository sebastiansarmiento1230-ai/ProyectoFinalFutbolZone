from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.reserva_schema import ReservaSchema, ReservaUpdateSchema
from app.controllers.reserva_controller import (
    get_reservas, get_reserva, get_reservas_usuario,
    create_reserva, update_reserva, delete_reserva
)
from app.models.reserva_model import ReservaModel
from app.utils.auth import get_admin_actual, get_usuario_actual

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])

# ── Rutas estáticas primero ─────────────────────────────
@router.get("/mis-reservas")
def mis_reservas(db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    usuario_id = int(usuario_actual.get("sub", 0))
    return get_reservas_usuario(usuario_id, db)

# ── Admin: listar todas las reservas ────────────────────
@router.get("/")
def listar(db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return get_reservas(db)

# ── Cliente/Admin: crear reserva (siempre queda PENDIENTE) ─
@router.post("/")
def crear(body: ReservaSchema, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    usuario_id = int(usuario_actual.get("sub", 0))
    return create_reserva(body, usuario_id, db)

# ── Obtener detalle (solo dueño o admin) ────────────────
@router.get("/{id}")
def obtener(id: int, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    reserva = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if reserva:
        es_admin = usuario_actual.get("rol") == "admin"
        es_dueno = int(usuario_actual.get("sub", 0)) == reserva.usuario_id
        if not es_admin and not es_dueno:
            raise HTTPException(status_code=403, detail="No tienes permiso para ver esta reserva")
    return get_reserva(id, db)

# ── Actualizar reserva (solo admin puede cambiar estado; dueño/admin otros campos) ─
@router.put("/{id}")
def actualizar(id: int, body: ReservaUpdateSchema, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    reserva = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    es_admin = usuario_actual.get("rol") == "admin"
    es_dueno = int(usuario_actual.get("sub", 0)) == reserva.usuario_id

    if not es_admin and not es_dueno:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta reserva")

    if body.estado is not None and not es_admin:
        raise HTTPException(status_code=403, detail="Solo el administrador puede aprobar, rechazar o cambiar el estado de una reserva")

    return update_reserva(id, body, db)

# ── Cancelar reserva (solo dueño o admin) ───────────────
@router.delete("/{id}")
def cancelar(id: int, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    reserva = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if reserva:
        es_admin = usuario_actual.get("rol") == "admin"
        es_dueno = int(usuario_actual.get("sub", 0)) == reserva.usuario_id
        if not es_admin and not es_dueno:
            raise HTTPException(status_code=403, detail="No tienes permiso para cancelar esta reserva")
    return delete_reserva(id, db)

# ── Cambiar estado directo (solo admin) ─────────────────
@router.patch("/{id}/estado")
def cambiar_estado(id: int, estado: str, db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    body = ReservaUpdateSchema(estado=estado)
    return update_reserva(id, body, db)
