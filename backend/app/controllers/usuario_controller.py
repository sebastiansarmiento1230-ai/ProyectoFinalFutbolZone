from sqlalchemy.orm import Session

from app.models.usuario_model import UsuarioModel, RolUsuario
from app.schemas.usuario_schema import UsuarioSchema, UsuarioUpdateSchema, UsuarioLoginSchema
from app.utils.auth import hash_password, verificar_password, crear_token
from app.utils.response import api_response


# ================================================
# GET ALL USUARIOS
# ================================================
def get_usuarios(db: Session):
    usuarios = db.query(UsuarioModel).all()
    data = [
        {
            "id": u.id,
            "nombre": u.nombre,
            "apellido": u.apellido,
            "email": u.email,
            "telefono": u.telefono,
            "rol": u.rol,
            "activo": u.activo,
            "creado_en": str(u.creado_en) if u.creado_en else None
        }
        for u in usuarios
    ]
    return api_response(True, "Lista de usuarios", data=data)


# ================================================
# GET USUARIO BY ID
# ================================================
def get_usuario(id: int, db: Session):
    u = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not u:
        return api_response(False, "Usuario no encontrado", error="Not found")
    data = {
        "id": u.id, "nombre": u.nombre, "apellido": u.apellido,
        "email": u.email, "telefono": u.telefono,
        "rol": u.rol, "activo": u.activo
    }
    return api_response(True, "Usuario encontrado", data=data)


# ================================================
# CLIENTES (rol=cliente)
# ================================================
def get_clientes(db: Session):
    clientes = db.query(UsuarioModel).filter(UsuarioModel.rol == RolUsuario.cliente).all()
    data = [
        {
            "id": c.id, "nombre": c.nombre, "apellido": c.apellido,
            "email": c.email, "telefono": c.telefono,
            "activo": c.activo,
            "total_reservas": len(c.reservas)
        }
        for c in clientes
    ]
    return api_response(True, "Lista de clientes", data=data)


# ================================================
# REGISTRO
# ================================================
def create_usuario(body: UsuarioSchema, db: Session):
    existe = db.query(UsuarioModel).filter(UsuarioModel.email == body.correo).first()
    if existe:
        return api_response(False, "El correo ya está registrado", error="Duplicate email")

    nuevo = UsuarioModel(
        nombre=body.nombre,
        apellido=body.apellido,
        email=body.correo,
        telefono=body.telefono,
        password_hash=hash_password(body.password),
        rol=RolUsuario.cliente
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return api_response(
        True,
        f"Usuario registrado correctamente. ¡Ya puedes iniciar sesión!",
        data={"id": nuevo.id, "nombre": nuevo.nombre, "email": nuevo.email}
    )


# ================================================
# LOGIN
# ================================================
def login_usuario(body: UsuarioLoginSchema, db: Session):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == body.correo).first()
    if not usuario or not verificar_password(body.password, usuario.password_hash):
        return api_response(False, "Correo o contraseña incorrectos", error="Unauthorized")
    if not usuario.activo:
        return api_response(False, "Cuenta desactivada", error="Forbidden")

    token = crear_token({"sub": usuario.id, "rol": usuario.rol, "nombre": usuario.nombre})
    return api_response(True, "Login exitoso", data={
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "rol": usuario.rol,
            "username": usuario.username or f"@{usuario.nombre.lower()}{usuario.id}",
            "posicion": usuario.posicion or "Delantero",
            "pie_habil": usuario.pie_habil or "Derecho",
            "dorsal": usuario.dorsal or 10,
            "bio": usuario.bio or "Jugador apasionado en FutbolZone ⚽",
            "avatar": usuario.avatar or f"https://api.dicebear.com/7.x/bottts/svg?seed={usuario.nombre}{usuario.id}"
        }
    })


# ================================================
# UPDATE USUARIO
# ================================================
def update_usuario(id: int, body: UsuarioUpdateSchema, db: Session):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not usuario:
        return api_response(False, "Usuario no encontrado", error="Not found")

    cambios = body.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return api_response(True, "Usuario actualizado correctamente",
                        data={"id": usuario.id, "nombre": usuario.nombre})


# ================================================
# DELETE USUARIO (desactivar)
# ================================================
def delete_usuario(id: int, db: Session):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not usuario:
        return api_response(False, "Usuario no encontrado", error="Not found")
    usuario.activo = False
    db.commit()
    return api_response(True, "Usuario desactivado correctamente")


# ================================================
# CAMBIAR ROL (admin puede hacer a alguien admin)
# ================================================
def cambiar_rol(id: int, rol: str, db: Session):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not usuario:
        return api_response(False, "Usuario no encontrado", error="Not found")
    if rol not in [r.value for r in RolUsuario]:
        return api_response(False, "Rol inválido", error="Bad request")
    usuario.rol = rol
    db.commit()
    return api_response(True, f"Rol actualizado a '{rol}'", data={"id": usuario.id})


# =======================================================
# PERFIL DEPORTIVO DEL JUGADOR
# =======================================================
def get_perfil_deportivo(id: int, db: Session):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not usuario:
        return api_response(False, "Jugador no encontrado", error="Not found")

    from app.models.calificacion_model import CalificacionJugadorModel
    califs = db.query(CalificacionJugadorModel).filter(CalificacionJugadorModel.jugador_id == id).all()
    total_califs = len(califs)
    promedio_rating = round(sum(c.estrellas for c in califs) / total_califs, 1) if total_califs > 0 else 5.0

    reservas_total = len(usuario.reservas) if usuario.reservas else 0
    reservas_completadas = sum(1 for r in usuario.reservas if r.estado in ["confirmada", "completada"]) if usuario.reservas else 0

    data = {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "nombre_completo": f"{usuario.nombre} {usuario.apellido}",
        "email": usuario.email,
        "telefono": usuario.telefono or "Sin teléfono",
        "rol": usuario.rol,
        "username": usuario.username or f"@{usuario.nombre.lower()}{usuario.id}",
        "posicion": usuario.posicion or "Delantero",
        "pie_habil": usuario.pie_habil or "Derecho",
        "dorsal": usuario.dorsal or 10,
        "bio": usuario.bio or "Jugador apasionado en FutbolZone ⚽",
        "avatar": usuario.avatar or f"https://api.dicebear.com/7.x/bottts/svg?seed={usuario.nombre}{usuario.id}",
        "fecha_registro": str(usuario.creado_en) if usuario.creado_en else "2026-01-01",
        "estadisticas": {
            "partidos_totales": reservas_total,
            "partidos_completados": reservas_completadas,
            "calificacion_promedio": promedio_rating,
            "total_valoraciones": total_califs
        },
        "opiniones_recibidas": [
            {
                "id": c.id,
                "evaluador_id": c.evaluador_id,
                "evaluador_nombre": f"{c.evaluador.nombre} {c.evaluador.apellido}" if c.evaluador else "Compañero",
                "evaluador_avatar": c.evaluador.avatar if c.evaluador else None,
                "estrellas": c.estrellas,
                "comentario": c.comentario,
                "fecha": str(c.creado_en)
            }
            for c in califs
        ]
    }
    return api_response(True, "Ficha deportiva del jugador", data=data)


def update_perfil_deportivo(id: int, datos: dict, db: Session):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not usuario:
        return api_response(False, "Jugador no encontrado", error="Not found")

    if "nombre" in datos and datos["nombre"]:
        usuario.nombre = datos["nombre"].strip()
    if "apellido" in datos and datos["apellido"]:
        usuario.apellido = datos["apellido"].strip()
    if "telefono" in datos:
        usuario.telefono = datos["telefono"].strip()
    if "username" in datos and datos["username"]:
        u = datos["username"].strip()
        usuario.username = u if u.startswith("@") else f"@{u}"
    if "posicion" in datos and datos["posicion"]:
        usuario.posicion = datos["posicion"].strip()
    if "pie_habil" in datos and datos["pie_habil"]:
        usuario.pie_habil = datos["pie_habil"].strip()
    if "dorsal" in datos and datos["dorsal"] is not None:
        try:
            usuario.dorsal = int(datos["dorsal"])
        except ValueError:
            pass
    if "bio" in datos:
        usuario.bio = datos["bio"].strip()
    if "avatar" in datos and datos["avatar"]:
        usuario.avatar = datos["avatar"].strip()

    db.commit()
    db.refresh(usuario)
    return get_perfil_deportivo(id, db)


def get_comunidad_jugadores(db: Session):
    from app.models.calificacion_model import CalificacionJugadorModel
    jugadores = db.query(UsuarioModel).filter(UsuarioModel.activo == True).all()

    lista = []
    for j in jugadores:
        califs = db.query(CalificacionJugadorModel).filter(CalificacionJugadorModel.jugador_id == j.id).all()
        promedio = round(sum(c.estrellas for c in califs) / len(califs), 1) if califs else 5.0
        lista.append({
            "id": j.id,
            "nombre": j.nombre,
            "apellido": j.apellido,
            "nombre_completo": f"{j.nombre} {j.apellido}",
            "email": j.email,
            "username": j.username or f"@{j.nombre.lower()}{j.id}",
            "posicion": j.posicion or "Delantero",
            "dorsal": j.dorsal or 10,
            "pie_habil": j.pie_habil or "Derecho",
            "avatar": j.avatar or f"https://api.dicebear.com/7.x/bottts/svg?seed={j.nombre}{j.id}",
            "bio": j.bio or "Jugador en FutbolZone ⚽",
            "calificacion": promedio,
            "total_opiniones": len(califs),
            "total_partidos": len(j.reservas) if j.reservas else 0
        })

    return api_response(True, "Comunidad de deportistas", data=lista)

