from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.calificacion_model import CalificacionJugadorModel, CalificacionServicioModel
from app.models.usuario_model import UsuarioModel
from app.models.reserva_model import ReservaModel, EstadoReserva
from app.utils.response import api_response


# =======================================================
# CALIFICACIONES ENTRE JUGADORES (PEER-TO-PEER)
# =======================================================
def calificar_jugador(evaluador_id: int, body: dict, db: Session):
    jugador_id = body.get("jugador_id")
    estrellas = int(body.get("estrellas", 5))
    comentario = body.get("comentario", "").strip()

    if not jugador_id:
        return api_response(False, "ID de jugador requerido", error="Bad request")

    if evaluador_id == jugador_id:
        return api_response(False, "Un jugador no puede calificarse a sí mismo", error="Forbidden")

    if estrellas < 1 or estrellas > 5:
        return api_response(False, "La calificación debe ser entre 1 y 5 estrellas", error="Validation error")

    # Verificar existencia del jugador
    jugador = db.query(UsuarioModel).filter(UsuarioModel.id == jugador_id).first()
    if not jugador:
        return api_response(False, "Jugador no encontrado", error="Not found")

    # Verificar si ya lo calificó previamente
    existente = db.query(CalificacionJugadorModel).filter(
        CalificacionJugadorModel.evaluador_id == evaluador_id,
        CalificacionJugadorModel.jugador_id == jugador_id
    ).first()

    if existente:
        existente.estrellas = estrellas
        existente.comentario = comentario
        db.commit()
        db.refresh(existente)
        return api_response(True, "Calificación actualizada exitosamente", data={"id": existente.id, "estrellas": existente.estrellas})

    nueva = CalificacionJugadorModel(
        evaluador_id=evaluador_id,
        jugador_id=jugador_id,
        estrellas=estrellas,
        comentario=comentario
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return api_response(True, "Calificación registrada correctamente", data={"id": nueva.id, "estrellas": nueva.estrellas})


def get_calificaciones_jugador(jugador_id: int, db: Session):
    califs = db.query(CalificacionJugadorModel).filter(CalificacionJugadorModel.jugador_id == jugador_id).all()
    total = len(califs)
    promedio = round(sum(c.estrellas for c in califs) / total, 1) if total > 0 else 5.0

    data = {
        "jugador_id": jugador_id,
        "total_calificaciones": total,
        "promedio": promedio,
        "opiniones": [
            {
                "id": c.id,
                "evaluador_nombre": f"{c.evaluador.nombre} {c.evaluador.apellido}" if c.evaluador else "Compañero",
                "evaluador_avatar": c.evaluador.avatar if c.evaluador else None,
                "estrellas": c.estrellas,
                "comentario": c.comentario,
                "fecha": str(c.creado_en)
            }
            for c in califs
        ]
    }
    return api_response(True, "Opiniones del jugador", data=data)


# =======================================================
# CALIFICACIÓN DEL SERVICIO POST-RESERVA (4 DIMENSIONES)
# =======================================================
def calificar_servicio(usuario_id: int, body: dict, db: Session):
    reserva_id = body.get("reserva_id")
    atencion = int(body.get("atencion", 5))
    servicio = int(body.get("servicio", 5))
    instalaciones = int(body.get("instalaciones", 5))
    experiencia = int(body.get("experiencia", 5))
    comentario = body.get("comentario", "").strip()

    if not reserva_id:
        return api_response(False, "ID de reserva requerido", error="Bad request")

    reserva = db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
    if not reserva:
        return api_response(False, "Reserva no encontrada", error="Not found")

    if reserva.usuario_id != usuario_id:
        return api_response(False, "No puedes calificar una reserva de otro usuario", error="Unauthorized")

    # Verificar que no esté ya calificada
    ya_calificada = db.query(CalificacionServicioModel).filter(CalificacionServicioModel.reserva_id == reserva_id).first()
    if ya_calificada:
        return api_response(False, "Esta reserva ya fue calificada previamente", error="Conflict")

    promedio = round((atencion + servicio + instalaciones + experiencia) / 4.0, 1)

    nueva = CalificacionServicioModel(
        reserva_id=reserva_id,
        usuario_id=usuario_id,
        cancha_id=reserva.cancha_id,
        atencion=atencion,
        servicio=servicio,
        instalaciones=instalaciones,
        experiencia=experiencia,
        promedio=promedio,
        comentario=comentario
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return api_response(True, "¡Gracias por calificar tu experiencia en FutbolZone!", data={"id": nueva.id, "promedio": nueva.promedio})


def get_calificaciones_servicio_admin(db: Session):
    items = db.query(CalificacionServicioModel).order_by(CalificacionServicioModel.creado_en.desc()).all()
    total = len(items)

    if total > 0:
        prom_atencion = round(sum(i.atencion for i in items) / total, 1)
        prom_servicio = round(sum(i.servicio for i in items) / total, 1)
        prom_instalaciones = round(sum(i.instalaciones for i in items) / total, 1)
        prom_experiencia = round(sum(i.experiencia for i in items) / total, 1)
        prom_general = round(sum(i.promedio for i in items) / total, 1)
    else:
        prom_atencion = prom_servicio = prom_instalaciones = prom_experiencia = prom_general = 5.0

    data = {
        "total_opiniones": total,
        "promedios": {
            "general": prom_general,
            "atencion": prom_atencion,
            "servicio": prom_servicio,
            "instalaciones": prom_instalaciones,
            "experiencia": prom_experiencia,
        },
        "listado": [
            {
                "id": i.id,
                "reserva_id": i.reserva_id,
                "cancha_nombre": i.cancha.nombre if i.cancha else "Cancha",
                "cliente_nombre": f"{i.usuario.nombre} {i.usuario.apellido}" if i.usuario else "Cliente",
                "atencion": i.atencion,
                "servicio": i.servicio,
                "instalaciones": i.instalaciones,
                "experiencia": i.experiencia,
                "promedio": i.promedio,
                "comentario": i.comentario,
                "fecha": str(i.creado_en)
            }
            for i in items
        ]
    }
    return api_response(True, "Auditoría de calificaciones del servicio", data=data)
