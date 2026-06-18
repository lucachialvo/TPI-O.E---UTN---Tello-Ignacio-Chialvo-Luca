import csv
import os
from datetime import datetime
from typing import Optional, List

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from database.models import Usuario, SolicitudProveedor, Proveedor, EstadoSolicitud


class Database:
    def __init__(self):
        self.usuarios_csv = config.USUARIOS_CSV
        self.solicitudes_csv = config.SOLICITUDES_CSV
        self.proveedores_csv = config.PROVEEDORES_CSV

    def _get_next_id(self, filepath: str) -> int:
        if not os.path.exists(filepath):
            return 1
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            max_id = 0
            for row in reader:
                row_id = int(row["id"])
                if row_id > max_id:
                    max_id = row_id
            return max_id + 1

    def _ensure_file(self, filepath: str, headers: List[str]):
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()

    def init_csv_files(self):
        self._ensure_file(self.usuarios_csv, ["id", "telegram_id", "nombre", "estado_actual", "fecha_inicio"])
        self._ensure_file(self.solicitudes_csv, ["id", "telegram_usuario", "razon_social", "cuit", "contacto", "telefono", "email", "direccion", "rubro", "descripcion", "estado", "fecha_creacion"])
        self._ensure_file(self.proveedores_csv, ["id", "razon_social", "cuit", "contacto", "telefono", "email", "direccion", "rubro", "descripcion", "fecha_alta"])

    def get_usuario(self, telegram_id: int) -> Optional[Usuario]:
        if not os.path.exists(self.usuarios_csv):
            return None
        with open(self.usuarios_csv, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["telegram_id"]) == telegram_id:
                    return Usuario.from_dict(row)
        return None

    def crear_o_actualizar_usuario(self, telegram_id: int, estado: str, nombre: Optional[str] = None) -> Usuario:
        usuario = self.get_usuario(telegram_id)
        if usuario:
            usuario.estado_actual = estado
            if nombre:
                usuario.nombre = nombre
            self._update_usuario(usuario)
        else:
            usuario = Usuario(
                id=self._get_next_id(self.usuarios_csv),
                telegram_id=telegram_id,
                nombre=nombre,
                estado_actual=estado,
                fecha_inicio=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            self._add_usuario(usuario)
        return usuario

    def _add_usuario(self, usuario: Usuario):
        with open(self.usuarios_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "telegram_id", "nombre", "estado_actual", "fecha_inicio"])
            writer.writerow(usuario.to_dict())

    def _update_usuario(self, usuario: Usuario):
        rows = []
        with open(self.usuarios_csv, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["telegram_id"]) == usuario.telegram_id:
                    row["estado_actual"] = usuario.estado_actual
                    row["nombre"] = usuario.nombre or ""
                rows.append(row)
        with open(self.usuarios_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "telegram_id", "nombre", "estado_actual", "fecha_inicio"])
            writer.writeheader()
            writer.writerows(rows)

    def crear_solicitud(self, solicitud: SolicitudProveedor) -> int:
        solicitud.id = self._get_next_id(self.solicitudes_csv)
        solicitud.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        solicitud.estado = EstadoSolicitud.PENDIENTE_REVISION
        with open(self.solicitudes_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "telegram_usuario", "razon_social", "cuit", "contacto", "telefono", "email", "direccion", "rubro", "descripcion", "estado", "fecha_creacion"])
            writer.writerow(solicitud.to_dict())
        return solicitud.id

    def get_solicitud(self, solicitud_id: int) -> Optional[SolicitudProveedor]:
        if not os.path.exists(self.solicitudes_csv):
            return None
        with open(self.solicitudes_csv, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["id"]) == solicitud_id:
                    return SolicitudProveedor.from_dict(row)
        return None

    def get_solicitudes_pendientes(self) -> List[SolicitudProveedor]:
        solicitudes = []
        if not os.path.exists(self.solicitudes_csv):
            return solicitudes
        with open(self.solicitudes_csv, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["estado"] == EstadoSolicitud.PENDIENTE_REVISION:
                    solicitudes.append(SolicitudProveedor.from_dict(row))
        return solicitudes

    def actualizar_estado_solicitud(self, solicitud_id: int, nuevo_estado: str):
        rows = []
        with open(self.solicitudes_csv, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["id"]) == solicitud_id:
                    row["estado"] = nuevo_estado
                rows.append(row)
        with open(self.solicitudes_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "telegram_usuario", "razon_social", "cuit", "contacto", "telefono", "email", "direccion", "rubro", "descripcion", "estado", "fecha_creacion"])
            writer.writeheader()
            writer.writerows(rows)

    def proveedor_existe_por_cuit(self, cuit: str) -> bool:
        if not os.path.exists(self.proveedores_csv):
            return False
        with open(self.proveedores_csv, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["cuit"] == cuit:
                    return True
        return False

    def crear_proveedor(self, solicitud: SolicitudProveedor) -> int:
        proveedor = Proveedor(
            id=self._get_next_id(self.proveedores_csv),
            razon_social=solicitud.razon_social,
            cuit=solicitud.cuit,
            contacto=solicitud.contacto,
            telefono=solicitud.telefono,
            email=solicitud.email,
            direccion=solicitud.direccion,
            rubro=solicitud.rubro,
            descripcion=solicitud.descripcion,
            fecha_alta=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        with open(self.proveedores_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "razon_social", "cuit", "contacto", "telefono", "email", "direccion", "rubro", "descripcion", "fecha_alta"])
            writer.writerow(proveedor.to_dict())
        return proveedor.id
