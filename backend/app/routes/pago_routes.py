from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.pago_model import PagoModel
from app.schemas.pago_schema import PagoSchema, PagoUpdateSchema
from app.controllers.pago_controller import (
    get_pagos, get_pago, get_pagos_usuario,
    create_pago, update_pago, delete_pago, get_resumen_pagos
)
from app.utils.auth import get_admin_actual, get_usuario_actual

router = APIRouter(prefix="/api/pagos", tags=["Pagos"])

# ── Admin ─────────────────────────────────────
@router.get("/")
def listar(db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return get_pagos(db)


@router.get("/resumen")
def resumen(db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return get_resumen_pagos(db)


@router.get("/mis-pagos")
def mis_pagos(db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    usuario_id = int(usuario_actual.get("sub", 0))
    return get_pagos_usuario(usuario_id, db)


@router.put("/{id}")
def actualizar(id: int, body: PagoUpdateSchema, db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return update_pago(id, body, db)


@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return delete_pago(id, db)


@router.get("/{id}")
def obtener(id: int, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    pago = db.query(PagoModel).filter(PagoModel.id == id).first()
    if pago:
        es_admin = usuario_actual.get("rol") == "admin"
        es_dueno = int(usuario_actual.get("sub", 0)) == pago.usuario_id
        if not es_admin and not es_dueno:
            raise HTTPException(status_code=403, detail="No tienes permiso para ver este pago")
    return get_pago(id, db)


@router.post("/")
def registrar(body: PagoSchema, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    usuario_id = int(usuario_actual.get("sub", 0))
    return create_pago(body, usuario_id, db)
