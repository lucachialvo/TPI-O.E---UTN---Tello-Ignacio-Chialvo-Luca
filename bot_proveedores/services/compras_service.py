from typing import Optional, Tuple

from database.db import Database
from database.models import SolicitudProveedor


class ComprasService:
    def __init__(self, db: Database):
        self.db = db

    def obtener_solicitudes_pendientes(self):
        return self.db.get_solicitudes_pendientes()

    def obtener_solicitud(self, solicitud_id: int) -> Optional[SolicitudProveedor]:
        return self.db.get_solicitud(solicitud_id)

    def aprobar_solicitud(self, solicitud_id: int) -> Tuple[bool, str, Optional[int]]:
        solicitud = self.db.get_solicitud(solicitud_id)
        if not solicitud:
            return False, f"No se encontró la solicitud #{solicitud_id}.", None
        
        if solicitud.estado != "PENDIENTE_REVISION":
            return False, f"La solicitud #{solicitud_id} no está pendiente de revisión (estado actual: {solicitud.estado}).", None
        
        if self.db.proveedor_existe_por_cuit(solicitud.cuit):
            return False, f"Ya existe un proveedor registrado con el CUIT {solicitud.cuit}.", None
        
        self.db.actualizar_estado_solicitud(solicitud_id, "APROBADO")
        proveedor_id = self.db.crear_proveedor(solicitud)
        return True, f"Solicitud #{solicitud_id} aprobada. Proveedor '{solicitud.razon_social}' registrado.", proveedor_id

    def rechazar_solicitud(self, solicitud_id: int) -> Tuple[bool, str]:
        solicitud = self.db.get_solicitud(solicitud_id)
        if not solicitud:
            return False, f"No se encontró la solicitud #{solicitud_id}."
        
        if solicitud.estado != "PENDIENTE_REVISION":
            return False, f"La solicitud #{solicitud_id} no está pendiente de revisión (estado actual: {solicitud.estado})."
        
        self.db.actualizar_estado_solicitud(solicitud_id, "RECHAZADO")
        return True, f"Solicitud #{solicitud_id} rechazada."
