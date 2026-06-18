import argparse
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

import config
from database.db import Database
from bot.handlers import Handlers
from bot.states import ChatState

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception while handling an update: {context.error}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Inicializar archivos CSV")
    args = parser.parse_args()

    db = Database()
    
    if args.init:
        db.init_csv_files()
        print("Archivos CSV inicializados correctamente.")
        return

    handlers = Handlers(db)

    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", handlers.cmd_start)],
        states={
            ChatState.REGISTRANDO_RAZON_SOCIAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, 
                    lambda u, c: handlers.handle_text(u, c, ChatState.REGISTRANDO_RAZON_SOCIAL))
            ],
            ChatState.REGISTRANDO_CUIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                    lambda u, c: handlers.handle_text(u, c, ChatState.REGISTRANDO_CUIT))
            ],
            ChatState.REGISTRANDO_CONTACTO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                    lambda u, c: handlers.handle_text(u, c, ChatState.REGISTRANDO_CONTACTO))
            ],
            ChatState.REGISTRANDO_TELEFONO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                    lambda u, c: handlers.handle_text(u, c, ChatState.REGISTRANDO_TELEFONO))
            ],
            ChatState.REGISTRANDO_EMAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                    lambda u, c: handlers.handle_text(u, c, ChatState.REGISTRANDO_EMAIL))
            ],
            ChatState.REGISTRANDO_DIRECCION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                    lambda u, c: handlers.handle_text(u, c, ChatState.REGISTRANDO_DIRECCION))
            ],
            ChatState.REGISTRANDO_RUBRO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                    lambda u, c: handlers.handle_text(u, c, ChatState.REGISTRANDO_RUBRO))
            ],
            ChatState.REGISTRANDO_DESCRIPCION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                    lambda u, c: handlers.handle_text(u, c, ChatState.REGISTRANDO_DESCRIPCION))
            ],
            ChatState.VALIDANDO_DATOS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                    lambda u, c: handlers.handle_text(u, c, ChatState.VALIDANDO_DATOS))
            ],
            ChatState.ESPERANDO_APROBACION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.unknown_command)
            ],
        },
        fallbacks=[
            CommandHandler("cancelar", handlers.cmd_cancelar),
            CommandHandler("start", handlers.cmd_start),
        ],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("cancelar", handlers.cmd_cancelar))
    application.add_handler(CommandHandler("ayuda", handlers.cmd_ayuda))
    application.add_handler(CommandHandler("estado", handlers.cmd_estado))
    application.add_handler(CommandHandler("solicitudes", handlers.cmd_solicitudes))
    application.add_handler(CommandHandler("solicitud", handlers.cmd_solicitud))
    application.add_handler(CommandHandler("aprobar", handlers.cmd_aprobar))
    application.add_handler(CommandHandler("rechazar", handlers.cmd_rechazar))
    application.add_handler(MessageHandler(filters.COMMAND, handlers.unknown_command))

    application.add_error_handler(error_handler)

    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
