from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.usuario_schema import UsuarioSchema, UsuarioUpdateSchema, UsuarioLoginSchema
from app.controllers.usuario_controller import (
    get_usuarios, get_usuario, get_clientes,
    create_usuario, login_usuario,
    update_usuario, delete_usuario, cambiar_rol,
    get_perfil_deportivo, update_perfil_deportivo, get_comunidad_jugadores
)
from app.utils.auth import get_admin_actual, get_usuario_actual

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

# ── Públicos ────────────────────────────────────────────
@router.post("/registro")
def registrar(body: UsuarioSchema, db: Session = Depends(get_db)):
    return create_usuario(body, db)

@router.post("/login")
def login(body: UsuarioLoginSchema, db: Session = Depends(get_db)):
    return login_usuario(body, db)

# ── Admin ────────────────────────────────────────────────
@router.get("/")
def listar(db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return get_usuarios(db)

@router.get("/clientes")
def listar_clientes(db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return get_clientes(db)

@router.get("/{id}")
def obtener(id: int, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    if usuario_actual.get("rol") != "admin" and int(usuario_actual.get("sub", 0)) != id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este perfil")
    return get_usuario(id, db)

@router.put("/{id}")
def actualizar(id: int, body: UsuarioUpdateSchema, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    es_admin = usuario_actual.get("rol") == "admin"
    if not es_admin and int(usuario_actual.get("sub", 0)) != id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este perfil")
    if not es_admin and body.activo is not None:
        raise HTTPException(status_code=403, detail="No tienes permiso para cambiar el estado activo de la cuenta")
    return update_usuario(id, body, db)

@router.patch("/{id}/rol")
def cambiar_rol_usuario(id: int, rol: str, db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return cambiar_rol(id, rol, db)

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), admin_actual: dict = Depends(get_admin_actual)):
    return delete_usuario(id, db)

# ── Perfil Deportivo & Comunidad ─────────────────────────
@router.get("/comunidad/deportistas")
def listar_comunidad(db: Session = Depends(get_db)):
    return get_comunidad_jugadores(db)

@router.get("/{id}/perfil-deportivo")
def ver_perfil_deportivo(id: int, db: Session = Depends(get_db)):
    return get_perfil_deportivo(id, db)

@router.put("/{id}/perfil-deportivo")
def guardar_perfil_deportivo(id: int, body: dict, db: Session = Depends(get_db), usuario_actual: dict = Depends(get_usuario_actual)):
    if usuario_actual.get("rol") != "admin" and int(usuario_actual.get("sub", 0)) != id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este perfil deportivo")
    return update_perfil_deportivo(id, body, db)
