from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int]
    telegram_id: int
    nombre: Optional[str]
    estado_actual: str
    fecha_inicio: str

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        return cls(
            id=int(data["id"]) if data.get("id") else None,
            telegram_id=int(data["telegram_id"]),
            nombre=data.get("nombre"),
            estado_actual=data.get("estado_actual", "INICIO"),
            fecha_inicio=data.get("fecha_inicio", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "nombre": self.nombre,
            "estado_actual": self.estado_actual,
            "fecha_inicio": self.fecha_inicio
        }


@dataclass
class SolicitudProveedor:
    id: Optional[int]
    telegram_usuario: int
    razon_social: str
    cuit: str
    contacto: str
    telefono: str
    email: str
    direccion: str
    rubro: str
    descripcion: str
    estado: str
    fecha_creacion: str

    @classmethod
    def from_dict(cls, data: dict) -> "SolicitudProveedor":
        return cls(
            id=int(data["id"]) if data.get("id") else None,
            telegram_usuario=int(data["telegram_usuario"]),
            razon_social=data["razon_social"],
            cuit=data["cuit"],
            contacto=data["contacto"],
            telefono=data["telefono"],
            email=data["email"],
            direccion=data["direccion"],
            rubro=data["rubro"],
            descripcion=data["descripcion"],
            estado=data["estado"],
            fecha_creacion=data["fecha_creacion"]
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "telegram_usuario": self.telegram_usuario,
            "razon_social": self.razon_social,
            "cuit": self.cuit,
            "contacto": self.contacto,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "rubro": self.rubro,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion
        }


@dataclass
class Proveedor:
    id: Optional[int]
    razon_social: str
    cuit: str
    contacto: str
    telefono: str
    email: str
    direccion: str
    rubro: str
    descripcion: str
    fecha_alta: str

    @classmethod
    def from_dict(cls, data: dict) -> "Proveedor":
        return cls(
            id=int(data["id"]) if data.get("id") else None,
            razon_social=data["razon_social"],
            cuit=data["cuit"],
            contacto=data["contacto"],
            telefono=data["telefono"],
            email=data["email"],
            direccion=data["direccion"],
            rubro=data["rubro"],
            descripcion=data["descripcion"],
            fecha_alta=data["fecha_alta"]
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "razon_social": self.razon_social,
            "cuit": self.cuit,
            "contacto": self.contacto,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "rubro": self.rubro,
            "descripcion": self.descripcion,
            "fecha_alta": self.fecha_alta
        }


class EstadoSolicitud:
    BORRADOR = "BORRADOR"
    PENDIENTE_REVISION = "PENDIENTE_REVISION"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"


class EstadoUsuario:
    INICIO = "INICIO"
    REGISTRANDO_RAZON_SOCIAL = "REGISTRANDO_RAZON_SOCIAL"
    REGISTRANDO_CUIT = "REGISTRANDO_CUIT"
    REGISTRANDO_CONTACTO = "REGISTRANDO_CONTACTO"
    REGISTRANDO_TELEFONO = "REGISTRANDO_TELEFONO"
    REGISTRANDO_EMAIL = "REGISTRANDO_EMAIL"
    REGISTRANDO_DIRECCION = "REGISTRANDO_DIRECCION"
    REGISTRANDO_RUBRO = "REGISTRANDO_RUBRO"
    REGISTRANDO_DESCRIPCION = "REGISTRANDO_DESCRIPCION"
    VALIDANDO_DATOS = "VALIDANDO_DATOS"
    ESPERANDO_APROBACION = "ESPERANDO_APROBACION"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"
