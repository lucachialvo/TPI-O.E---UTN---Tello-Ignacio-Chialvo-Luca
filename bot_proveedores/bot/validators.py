import re
from typing import Tuple


class Validators:
    @staticmethod
    def validar_cuit(cuit: str) -> Tuple[bool, str]:
        cuit_limpio = re.sub(r'[-\s]', '', cuit)
        if not cuit_limpio.isdigit():
            return False, "El CUIT debe contener solo números."
        if len(cuit_limpio) != 11:
            return False, "El CUIT debe tener exactamente 11 dígitos."
        return True, ""

    @staticmethod
    def validar_email(email: str) -> Tuple[bool, str]:
        if not email or not email.strip():
            return False, "El email es obligatorio."
        if '@' not in email:
            return False, "El correo debe contener el símbolo @."
        partes = email.split('@')
        if len(partes) != 2:
            return False, "El correo debe contener exactamente un @."
        usuario, dominio = partes
        if not usuario:
            return False, "El correo debe tener un usuario antes del @."
        if not dominio or '.' not in dominio:
            return False, "El correo debe tener un dominio con punto (ej: empresa.com)."
        if dominio.startswith('.') or dominio.endswith('.'):
            return False, "El dominio no puede empezar o terminar con punto."
        return True, ""

    @staticmethod
    def validar_telefono(telefono: str) -> Tuple[bool, str]:
        telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
        if telefono_limpio.startswith('+'):
            telefono_limpio = telefono_limpio[1:]
        if not telefono_limpio.isdigit():
            return False, "El teléfono debe contener solo números."
        if len(telefono_limpio) < 8 or len(telefono_limpio) > 15:
            return False, "El teléfono debe tener entre 8 y 15 dígitos."
        return True, ""

    @staticmethod
    def validar_no_vacio(campo: str, nombre: str) -> Tuple[bool, str]:
        if not campo or not campo.strip():
            return False, f"El campo {nombre} es obligatorio. Ingrese un valor."
        return True, ""

    @staticmethod
    def normalizar_cuit(cuit: str) -> str:
        return re.sub(r'[-\s]', '', cuit)
