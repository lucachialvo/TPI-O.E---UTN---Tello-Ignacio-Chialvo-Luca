from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from bot.validators import Validators
from bot.states import ChatState
from database.db import Database
from database.models import SolicitudProveedor


@dataclass
class DatosProveedor:
    razon_social: str = ""
    cuit: str = ""
    telefono: str = ""
    email: str = ""
    direccion: str = ""
    rubro: str = ""
    descripcion: str = ""
    telegram_usuario: int = 0


class ProveedorService:
    def __init__(self, db: Database):
        self.db = db

    def validar_campo(self, estado: str, valor: str) -> Tuple[bool, str]:
        if estado == ChatState.REGISTRANDO_RAZON_SOCIAL:
            return Validators.validar_no_vacio(valor, "Razón Social")
        elif estado == ChatState.REGISTRANDO_CUIT:
            return Validators.validar_cuit(valor)
        elif estado == ChatState.REGISTRANDO_TELEFONO:
            return Validators.validar_telefono(valor)
        elif estado == ChatState.REGISTRANDO_EMAIL:
            return Validators.validar_email(valor)
        elif estado == ChatState.REGISTRANDO_DIRECCION:
            return Validators.validar_no_vacio(valor, "Dirección")
        elif estado == ChatState.REGISTRANDO_RUBRO:
            return Validators.validar_no_vacio(valor, "Rubro")
        elif estado == ChatState.REGISTRANDO_DESCRIPCION:
            return Validators.validar_no_vacio(valor, "Descripción")
        return True, ""

    def obtener_mensaje_error_formato(self, estado: str) -> str:
        mensajes = {
            ChatState.REGISTRANDO_CUIT: "El CUIT debe contener solo números (11 dígitos).",
            ChatState.REGISTRANDO_EMAIL: "El correo ingresado no tiene formato válido. Ejemplo: ejemplo@empresa.com",
            ChatState.REGISTRANDO_TELEFONO: "El teléfono debe tener entre 8 y 15 dígitos numéricos.",
        }
        return mensajes.get(estado, "El valor ingresado no es válido.")

    def crear_solicitud(self, datos: DatosProveedor) -> int:
        solicitud = SolicitudProveedor(
            id=None,
            telegram_usuario=datos.telegram_usuario,
            razon_social=datos.razon_social,
            cuit=Validators.normalizar_cuit(datos.cuit),
            telefono=datos.telefono,
            email=datos.email,
            direccion=datos.direccion,
            rubro=datos.rubro,
            descripcion=datos.descripcion,
            estado="",
            fecha_creacion=""
        )
        return self.db.crear_solicitud(solicitud)
