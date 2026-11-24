from sqlalchemy.orm import Session
from datetime import datetime, date

from app.models.reserva_model import ReservaModel, EstadoReserva
from app.models.cancha_model import CanchaModel
from app.models.usuario_model import UsuarioModel
from app.schemas.reserva_schema import ReservaSchema, ReservaUpdateSchema
from app.utils.response import api_response
from app.controllers.notificacion_controller import (
    crear_notificacion,
    crear_notificacion_admins,
)


def _reserva_dict(r: ReservaModel, con_nombres: bool = True):
    d = {
        "id": r.id,
        "usuario_id": r.usuario_id,
        "cancha_id": r.cancha_id,
        "fecha": str(r.fecha),
        "hora_inicio": str(r.hora_inicio),
        "hora_fin": str(r.hora_fin),
        "precio_total": r.precio_total,
        "estado": r.estado.value if hasattr(r.estado, "value") else str(r.estado),
        "notas": r.notas,
        "creado_en": str(r.creado_en) if r.creado_en else None
    }
    if con_nombres:
        d["cliente"]          = f"{r.usuario.nombre} {r.usuario.apellido}" if r.usuario else "Cliente"
        d["cliente_nombre"]   = f"{r.usuario.nombre} {r.usuario.apellido}" if r.usuario else "Cliente"
        d["cliente_email"]    = r.usuario.email if r.usuario else ""
        d["cliente_telefono"] = r.usuario.telefono if r.usuario else ""
        d["cancha_nombre"]    = r.cancha.nombre if r.cancha else "Cancha"
        d["cancha_tipo"]      = r.cancha.tipo if r.cancha else "Sintética"
        d["cancha_precio_hora"] = r.cancha.precio_hora if r.cancha else 0
    return d


def get_reservas(db: Session):
    reservas = db.query(ReservaModel).order_by(ReservaModel.creado_en.desc()).all()
    return api_response(True, "Lista de reservas", data=[_reserva_dict(r) for r in reservas])


def get_reserva(id: int, db: Session):
    r = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if not r:
        return api_response(False, "Reserva no encontrada", error="Not found")
    return api_response(True, "Reserva encontrada", data=_reserva_dict(r))


def get_reservas_usuario(usuario_id: int, db: Session):
    reservas = (
        db.query(ReservaModel)
        .filter(ReservaModel.usuario_id == usuario_id)
        .order_by(ReservaModel.creado_en.desc())
        .all()
    )
    return api_response(True, "Mis reservas", data=[_reserva_dict(r) for r in reservas])


def create_reserva(body: ReservaSchema, usuario_id: int, db: Session):
    # Validar fecha y horario
    if body.fecha < date.today():
        return api_response(False, "No se pueden realizar reservas en fechas pasadas", error="Bad request")
    if body.hora_fin <= body.hora_inicio:
        return api_response(False, "La hora de fin debe ser posterior a la hora de inicio", error="Bad request")

    cancha = db.query(CanchaModel).filter(
        CanchaModel.id == body.cancha_id,
        CanchaModel.activa == True
    ).first()
    if not cancha:
        return api_response(False, "Cancha no encontrada o no disponible", error="Not found")

    # Verificar conflicto de horario (pendiente o confirmada)
    conflicto = db.query(ReservaModel).filter(
        ReservaModel.cancha_id == body.cancha_id,
        ReservaModel.fecha == body.fecha,
        ReservaModel.estado.in_([EstadoReserva.pendiente, EstadoReserva.confirmada]),
        ReservaModel.hora_inicio < body.hora_fin,
        ReservaModel.hora_fin > body.hora_inicio
    ).first()
    if conflicto:
        return api_response(False, "La cancha ya está reservada en ese horario", error="Conflict")

    # Calcular precio
    if body.precio_total is not None and body.precio_total > 0:
        precio = float(body.precio_total)
    else:
        inicio_dt = datetime.combine(datetime.today(), body.hora_inicio)
        fin_dt    = datetime.combine(datetime.today(), body.hora_fin)
        horas     = (fin_dt - inicio_dt).seconds / 3600
        costo_cancha  = horas * cancha.precio_hora
        extra_kit     = 15000 if (body.incluye_kit or (body.notas and "Kit: Sí" in body.notas)) else 0
        extra_arbitro = 30000 if (body.incluye_arbitro or (body.notas and "Árbitro: Sí" in body.notas)) else 0
        descuento     = body.descuento if body.descuento else 0
        precio        = max(costo_cancha + extra_kit + extra_arbitro - descuento, 0)
    precio = round(precio, 2)

    nueva = ReservaModel(
        usuario_id=usuario_id,
        cancha_id=body.cancha_id,
        fecha=body.fecha,
        hora_inicio=body.hora_inicio,
        hora_fin=body.hora_fin,
        precio_total=precio,
        estado=EstadoReserva.pendiente,   # ← siempre PENDIENTE al crear
        notas=body.notas
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # Obtener nombre del usuario que reservó
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    nombre_cliente = f"{usuario.nombre} {usuario.apellido}" if usuario else "Un cliente"

    # Notificación para todos los admins (en BD)
    crear_notificacion_admins(
        db=db,
        titulo="🆕 Nueva solicitud de reserva",
        mensaje=(
            f"{nombre_cliente} ha solicitado reservar {cancha.nombre} "
            f"para el {body.fecha} de {str(body.hora_inicio)[:5]} a {str(body.hora_fin)[:5]}. "
            f"Total: ${precio:,.0f} COP. Estado: PENDIENTE DE APROBACIÓN."
        ),
        tipo="reserva",
        reserva_id=nueva.id,
    )

    return api_response(
        True,
        "Reserva creada correctamente — Pendiente de aprobación por el administrador",
        data={
            "id": nueva.id,
            "precio_total": nueva.precio_total,
            "estado": nueva.estado.value,
        }
    )


def update_reserva(id: int, body: ReservaUpdateSchema, db: Session):
    reserva = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if not reserva:
        return api_response(False, "Reserva no encontrada", error="Not found")

    nuevo_estado = body.estado if body.estado else None

    if nuevo_estado == "confirmada":
        conflicto = db.query(ReservaModel).filter(
            ReservaModel.id != reserva.id,
            ReservaModel.cancha_id == reserva.cancha_id,
            ReservaModel.fecha == reserva.fecha,
            ReservaModel.estado == EstadoReserva.confirmada,
            ReservaModel.hora_inicio < reserva.hora_fin,
            ReservaModel.hora_fin > reserva.hora_inicio
        ).first()
        if conflicto:
            return api_response(
                False,
                "Ya existe otra reserva CONFIRMADA para esa cancha y horario",
                error="Conflict"
            )

    for campo, valor in body.model_dump(exclude_unset=True).items():
        if campo == "estado" and valor:
            # Mapear string a enum
            try:
                setattr(reserva, campo, EstadoReserva(valor))
            except ValueError:
                return api_response(False, f"Estado inválido: {valor}", error="Bad request")
        else:
            setattr(reserva, campo, valor)

    db.commit()
    db.refresh(reserva)

    # Disparar notificación al cliente según el nuevo estado
    if nuevo_estado:
        cancha_nombre = reserva.cancha.nombre if reserva.cancha else "la cancha"
        fecha_res     = str(reserva.fecha)

        if nuevo_estado == "confirmada":
            crear_notificacion(
                db=db,
                usuario_id=reserva.usuario_id,
                titulo="✅ ¡Reserva confirmada!",
                mensaje=(
                    f"¡Tu reserva ha sido ACEPTADA! Tu solicitud para {cancha_nombre} "
                    f"el {fecha_res} de {str(reserva.hora_inicio)[:5]} a {str(reserva.hora_fin)[:5]} "
                    f"ha sido confirmada. Te esperamos en la sede."
                ),
                tipo="reserva",
                reserva_id=reserva.id,
            )

        elif nuevo_estado == "rechazada":
            crear_notificacion(
                db=db,
                usuario_id=reserva.usuario_id,
                titulo="❌ Solicitud de reserva rechazada",
                mensaje=(
                    f"Tu solicitud para {cancha_nombre} el {fecha_res} "
                    f"ha sido rechazada por el administrador. "
                    f"Puedes consultar otros horarios disponibles."
                ),
                tipo="reserva",
                reserva_id=reserva.id,
            )

        elif nuevo_estado == "cancelada":
            crear_notificacion(
                db=db,
                usuario_id=reserva.usuario_id,
                titulo="🚫 Reserva cancelada",
                mensaje=(
                    f"Tu turno para {cancha_nombre} el {fecha_res} "
                    f"fue cancelado. El horario ha quedado disponible para nueva reserva."
                ),
                tipo="reserva",
                reserva_id=reserva.id,
            )

        elif nuevo_estado == "completada":
            crear_notificacion(
                db=db,
                usuario_id=reserva.usuario_id,
                titulo="🏆 ¡Partido completado!",
                mensaje=(
                    f"¡Gracias por jugar en FutbolZone! Tu partido en {cancha_nombre} "
                    f"el {fecha_res} fue registrado como completado."
                ),
                tipo="reserva",
                reserva_id=reserva.id,
            )

    return api_response(True, "Reserva actualizada correctamente", data={"id": reserva.id, "estado": reserva.estado.value})


def delete_reserva(id: int, db: Session):
    reserva = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if not reserva:
        return api_response(False, "Reserva no encontrada", error="Not found")
    reserva.estado = EstadoReserva.cancelada
    db.commit()

    cancha_nombre = reserva.cancha.nombre if reserva.cancha else "la cancha"
    fecha_res = str(reserva.fecha)
    nombre_cliente = f"{reserva.usuario.nombre} {reserva.usuario.apellido}" if reserva.usuario else "Un cliente"

    crear_notificacion(
        db=db,
        usuario_id=reserva.usuario_id,
        titulo="🚫 Reserva cancelada",
        mensaje=(
            f"Tu turno para {cancha_nombre} el {fecha_res} "
            f"fue cancelado. El horario ha quedado disponible."
        ),
        tipo="reserva",
        reserva_id=reserva.id,
    )
    crear_notificacion_admins(
        db=db,
        titulo="🚫 Reserva cancelada por usuario",
        mensaje=(
            f"{nombre_cliente} canceló la reserva #{reserva.id} en {cancha_nombre} "
            f"para el {fecha_res}."
        ),
        tipo="reserva",
        reserva_id=reserva.id,
    )
    return api_response(True, "Reserva cancelada correctamente")
