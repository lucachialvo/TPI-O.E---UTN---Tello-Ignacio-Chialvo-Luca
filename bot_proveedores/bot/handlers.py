from telegram import Update
from telegram.ext import ContextTypes

from bot.states import ChatState
from bot.validators import Validators
from database.db import Database
from services.proveedor_service import ProveedorService, DatosProveedor
from services.compras_service import ComprasService


class UserData:
    _instances = {}

    @classmethod
    def get(cls, user_id: int) -> "UserData":
        if user_id not in cls._instances:
            cls._instances[user_id] = cls()
            cls._instances[user_id].datos = DatosProveedor()
            cls._instances[user_id].datos.telegram_usuario = user_id
        return cls._instances[user_id]

    @classmethod
    def clear(cls, user_id: int):
        if user_id in cls._instances:
            del cls._instances[user_id]


class Handlers:
    def __init__(self, db: Database):
        self.db = db
        self.proveedor_service = ProveedorService(db)
        self.compras_service = ComprasService(db)

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        UserData.clear(user_id)
        self.db.crear_o_actualizar_usuario(user_id, ChatState.REGISTRANDO_RAZON_SOCIAL)
        
        await update.message.reply_text(
            "¡Bienvenido al sistema de registro de proveedores!\n"
            "Este bot le ayudará a registrar un nuevo proveedor en nuestra base de datos.\n"
            "Comenzaremos solicitando los datos del proveedor.\n\n"
            "Ingrese la RAZÓN SOCIAL del proveedor:"
        )
        return ChatState.REGISTRANDO_RAZON_SOCIAL

    async def cmd_cancelar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        UserData.clear(user_id)
        self.db.crear_o_actualizar_usuario(user_id, ChatState.CANCELADO)
        
        await update.message.reply_text(
            "Operación cancelada.\n"
            "Los datos ingresados han sido eliminados.\n"
            "Use /start para iniciar un nuevo registro."
        )
        return ChatState.CANCELADO

    async def cmd_ayuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Comandos disponibles:\n\n"
            "/start - Iniciar registro de proveedor\n"
            "/cancelar - Cancelar operación actual\n"
            "/estado - Ver estado del proceso\n"
            "/solicitudes - Ver solicitudes pendientes (Compras)\n"
            "/aprobar <id> - Aprobar solicitud (Compras)\n"
            "/rechazar <id> - Rechazar solicitud (Compras)\n"
            "/solicitud <id> - Ver detalle de solicitud (Compras)"
        )

    async def cmd_estado(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        usuario = self.db.get_usuario(user_id)
        
        if not usuario or usuario.estado_actual == ChatState.INICIO or usuario.estado_actual == ChatState.CANCELADO:
            await update.message.reply_text("No tiene ningún proceso activo. Use /start para iniciar.")
            return
        
        user_data = UserData.get(user_id)
        estado = ChatState.estado_a_campo(usuario.estado_actual)
        
        msg = f"Estado actual: {usuario.estado_actual}\n"
        if estado:
            msg += f"Campo actual: {estado}\n"
        
        if user_data.datos.razon_social:
            msg += f"\nDatos cargados:\n"
            if user_data.datos.razon_social:
                msg += f"  - Razón Social: {user_data.datos.razon_social}\n"
            if user_data.datos.cuit:
                msg += f"  - CUIT: {user_data.datos.cuit}\n"
            if user_data.datos.contacto:
                msg += f"  - Contacto: {user_data.datos.contacto}\n"
        
        await update.message.reply_text(msg)

    async def cmd_solicitudes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        solicitudes = self.compras_service.obtener_solicitudes_pendientes()
        
        if not solicitudes:
            await update.message.reply_text("No hay solicitudes pendientes de revisión.")
            return
        
        msg = "Solicitudes Pendientes:\n\n"
        for sol in solicitudes:
            msg += f"#{sol.id} - {sol.razon_social}\n"
            msg += f"  CUIT: {sol.cuit}\n"
            msg += f"  Estado: Pendiente revisión\n"
            msg += f"  Fecha: {sol.fecha_creacion}\n\n"
        
        await update.message.reply_text(msg)

    async def cmd_solicitud(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Uso: /solicitud <id>")
            return
        
        try:
            solicitud_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text("ID de solicitud inválido.")
            return
        
        solicitud = self.compras_service.obtener_solicitud(solicitud_id)
        if not solicitud:
            await update.message.reply_text(f"No se encontró la solicitud #{solicitud_id}.")
            return
        
        msg = (
            f"Solicitud #{solicitud.id}\n\n"
            f"Razón Social: {solicitud.razon_social}\n"
            f"CUIT: {solicitud.cuit}\n"
            f"Contacto: {solicitud.contacto}\n"
            f"Teléfono: {solicitud.telefono}\n"
            f"Email: {solicitud.email}\n"
            f"Dirección: {solicitud.direccion}\n"
            f"Rubro: {solicitud.rubro}\n"
            f"Descripción: {solicitud.descripcion}\n"
            f"Estado: {solicitud.estado}\n"
            f"Fecha de creación: {solicitud.fecha_creacion}\n"
            f"Solicitante (Telegram ID): {solicitud.telegram_usuario}"
        )
        await update.message.reply_text(msg)

    async def cmd_aprobar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Uso: /aprobar <id>")
            return
        
        try:
            solicitud_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text("ID de solicitud inválido.")
            return
        
        exito, mensaje, _ = self.compras_service.aprobar_solicitud(solicitud_id)
        await update.message.reply_text(mensaje)

    async def cmd_rechazar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Uso: /rechazar <id>")
            return
        
        try:
            solicitud_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text("ID de solicitud inválido.")
            return
        
        exito, mensaje = self.compras_service.rechazar_solicitud(solicitud_id)
        await update.message.reply_text(mensaje)

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE, estado_actual: str):
        user_id = update.effective_user.id
        texto = update.message.text.strip()
        user_data = UserData.get(user_id)
        
        if estado_actual == ChatState.REGISTRANDO_RAZON_SOCIAL:
            valido, error = self.proveedor_service.validar_campo(estado_actual, texto)
            if not valido:
                await update.message.reply_text(error)
                return estado_actual
            user_data.datos.razon_social = texto
            nuevo_estado = ChatState.siguiente_estado(estado_actual)
        
        elif estado_actual == ChatState.REGISTRANDO_CUIT:
            valido, error = self.proveedor_service.validar_campo(estado_actual, texto)
            if not valido:
                await update.message.reply_text(error)
                return estado_actual
            user_data.datos.cuit = texto
            nuevo_estado = ChatState.siguiente_estado(estado_actual)
        
        elif estado_actual == ChatState.REGISTRANDO_CONTACTO:
            valido, error = self.proveedor_service.validar_campo(estado_actual, texto)
            if not valido:
                await update.message.reply_text(error)
                return estado_actual
            user_data.datos.contacto = texto
            nuevo_estado = ChatState.siguiente_estado(estado_actual)
        
        elif estado_actual == ChatState.REGISTRANDO_TELEFONO:
            valido, error = self.proveedor_service.validar_campo(estado_actual, texto)
            if not valido:
                await update.message.reply_text(error)
                return estado_actual
            user_data.datos.telefono = texto
            nuevo_estado = ChatState.siguiente_estado(estado_actual)
        
        elif estado_actual == ChatState.REGISTRANDO_EMAIL:
            valido, error = self.proveedor_service.validar_campo(estado_actual, texto)
            if not valido:
                await update.message.reply_text(error)
                return estado_actual
            user_data.datos.email = texto
            nuevo_estado = ChatState.siguiente_estado(estado_actual)
        
        elif estado_actual == ChatState.REGISTRANDO_DIRECCION:
            valido, error = self.proveedor_service.validar_campo(estado_actual, texto)
            if not valido:
                await update.message.reply_text(error)
                return estado_actual
            user_data.datos.direccion = texto
            nuevo_estado = ChatState.siguiente_estado(estado_actual)
        
        elif estado_actual == ChatState.REGISTRANDO_RUBRO:
            valido, error = self.proveedor_service.validar_campo(estado_actual, texto)
            if not valido:
                await update.message.reply_text(error)
                return estado_actual
            user_data.datos.rubro = texto
            nuevo_estado = ChatState.siguiente_estado(estado_actual)
        
        elif estado_actual == ChatState.REGISTRANDO_DESCRIPCION:
            valido, error = self.proveedor_service.validar_campo(estado_actual, texto)
            if not valido:
                await update.message.reply_text(error)
                return estado_actual
            user_data.datos.descripcion = texto
            nuevo_estado = ChatState.VALIDANDO_DATOS
        
        elif estado_actual == ChatState.VALIDANDO_DATOS:
            solicitud_id = self.proveedor_service.crear_solicitud(user_data.datos)
            self.db.crear_o_actualizar_usuario(user_id, ChatState.ESPERANDO_APROBACION)
            UserData.clear(user_id)
            await update.message.reply_text(
                "Todos los datos han sido validados correctamente.\n"
                "Su solicitud ha sido enviada al Departamento de Compras para evaluación.\n"
                "Usted recibirá una notificación cuando el proceso finalice.\n"
                f"Estado: PENDIENTE_REVISION\n"
                f"ID de Solicitud: {solicitud_id}"
            )
            return ChatState.ESPERANDO_APROBACION
        
        else:
            await update.message.reply_text("No entiendo el comando. Use /ayuda para ver opciones.")
            return estado_actual
        
        self.db.crear_o_actualizar_usuario(user_id, nuevo_estado)
        campo = ChatState.estado_a_campo(nuevo_estado)
        await update.message.reply_text(f"✓ {campo} registrado.\n\nIngrese {campo}:")
        
        if nuevo_estado == ChatState.VALIDANDO_DATOS:
            return await self.handle_text(update, context, nuevo_estado)
        
        return nuevo_estado

    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("No entiendo el comando. Use /ayuda para ver opciones.")
