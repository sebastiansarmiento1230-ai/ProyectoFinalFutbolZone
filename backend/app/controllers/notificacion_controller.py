from sqlalchemy.orm import Session
from app.models.notificacion_model import NotificacionModel
from app.models.usuario_model import UsuarioModel, RolUsuario
from app.utils.response import api_response


def crear_notificacion(db: Session, usuario_id: int, titulo: str, mensaje: str,
                       tipo: str = "reserva", reserva_id: int = None):
    """Crea una notificación en la BD para un usuario específico."""
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        return None
    if reserva_id is not None:
        from app.models.reserva_model import ReservaModel
        reserva = db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
        if not reserva:
            reserva_id = None

    notif = NotificacionModel(
        usuario_id=usuario_id,
        titulo=titulo,
        mensaje=mensaje,
        tipo=tipo,
        reserva_id=reserva_id
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def crear_notificacion_admins(db: Session, titulo: str, mensaje: str,
                              tipo: str = "reserva", reserva_id: int = None):
    """Crea una notificación para TODOS los usuarios con rol admin."""
    admins = db.query(UsuarioModel).filter(
        UsuarioModel.rol == RolUsuario.admin,
        UsuarioModel.activo == True
    ).all()
    for admin in admins:
        notif = NotificacionModel(
            usuario_id=admin.id,
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo,
            reserva_id=reserva_id
        )
        db.add(notif)
    db.commit()


def _notif_dict(n: NotificacionModel) -> dict:
    return {
        "id": n.id,
        "usuario_id": n.usuario_id,
        "titulo": n.titulo,
        "mensaje": n.mensaje,
        "tipo": n.tipo,
        "leida": n.leida,
        "reserva_id": n.reserva_id,
        "creado_en": str(n.creado_en) if n.creado_en else None,
    }


def get_notificaciones_usuario(usuario_id: int, db: Session, solo_no_leidas: bool = False):
    q = db.query(NotificacionModel).filter(NotificacionModel.usuario_id == usuario_id)
    if solo_no_leidas:
        q = q.filter(NotificacionModel.leida == False)
    notifs = q.order_by(NotificacionModel.creado_en.desc()).limit(50).all()
    return api_response(True, "Notificaciones", data=[_notif_dict(n) for n in notifs])


def get_conteo_no_leidas(usuario_id: int, db: Session):
    conteo = db.query(NotificacionModel).filter(
        NotificacionModel.usuario_id == usuario_id,
        NotificacionModel.leida == False
    ).count()
    return api_response(True, "Conteo no leídas", data={"count": conteo})


def marcar_leida(notif_id: int, usuario_id: int, db: Session):
    notif = db.query(NotificacionModel).filter(
        NotificacionModel.id == notif_id,
        NotificacionModel.usuario_id == usuario_id
    ).first()
    if not notif:
        return api_response(False, "Notificación no encontrada", error="Not found")
    notif.leida = True
    db.commit()
    return api_response(True, "Notificación marcada como leída")


def marcar_todas_leidas(usuario_id: int, db: Session):
    db.query(NotificacionModel).filter(
        NotificacionModel.usuario_id == usuario_id,
        NotificacionModel.leida == False
    ).update({"leida": True})
    db.commit()
    return api_response(True, "Todas las notificaciones marcadas como leídas")
