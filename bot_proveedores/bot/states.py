class ChatState:
    INICIO = "INICIO"
    REGISTRANDO_RAZON_SOCIAL = "REGISTRANDO_RAZON_SOCIAL"
    REGISTRANDO_CUIT = "REGISTRANDO_CUIT"
    REGISTRANDO_TELEFONO = "REGISTRANDO_TELEFONO"
    REGISTRANDO_EMAIL = "REGISTRANDO_EMAIL"
    REGISTRANDO_DIRECCION = "REGISTRANDO_DIRECCION"
    REGISTRANDO_RUBRO = "REGISTRANDO_RUBRO"
    REGISTRANDO_DESCRIPCION = "REGISTRANDO_DESCRIPCION"
    VALIDANDO_DATOS = "VALIDANDO_DATOS"
    ESPERANDO_APROBACION = "ESPERANDO_APROBACION"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"

    STATES_REGISTRO = [
        REGISTRANDO_RAZON_SOCIAL,
        REGISTRANDO_CUIT,
        REGISTRANDO_TELEFONO,
        REGISTRANDO_EMAIL,
        REGISTRANDO_DIRECCION,
        REGISTRANDO_RUBRO,
        REGISTRANDO_DESCRIPCION,
    ]

    @staticmethod
    def siguiente_estado(estado_actual: str) -> str:
        flujo = [
            ChatState.REGISTRANDO_RAZON_SOCIAL,
            ChatState.REGISTRANDO_CUIT,
            ChatState.REGISTRANDO_TELEFONO,
            ChatState.REGISTRANDO_EMAIL,
            ChatState.REGISTRANDO_DIRECCION,
            ChatState.REGISTRANDO_RUBRO,
            ChatState.REGISTRANDO_DESCRIPCION,
        ]
        if estado_actual not in flujo:
            return flujo[0]
        idx = flujo.index(estado_actual)
        if idx == len(flujo) - 1:
            return ChatState.VALIDANDO_DATOS
        return flujo[idx + 1]

    @staticmethod
    def estado_a_campo(estado: str) -> str:
        mapeo = {
            ChatState.REGISTRANDO_RAZON_SOCIAL: "Razón Social",
            ChatState.REGISTRANDO_CUIT: "CUIT",
            ChatState.REGISTRANDO_TELEFONO: "Teléfono",
            ChatState.REGISTRANDO_EMAIL: "Email",
            ChatState.REGISTRANDO_DIRECCION: "Dirección",
            ChatState.REGISTRANDO_RUBRO: "Rubro",
            ChatState.REGISTRANDO_DESCRIPCION: "Descripción",
        }
        return mapeo.get(estado, "")

    @staticmethod
    def es_estado_registro(estado: str) -> bool:
        return estado in ChatState.STATES_REGISTRO
