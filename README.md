# Bot de Telegram - Alta de Proveedores

## Problema Empresarial

El proceso manual de alta de proveedores genera demoras y errores en la carga de información, carece de trazabilidad y requiere intervención humana en cada paso del proceso administrativo.

### Solución Propuesta

Automatizar el registro de nuevos proveedores mediante un chatbot de Telegram que siga el flujo BPMN definido, permitiendo que los empleados registren proveedores de forma autónoma y el Departamento de Compras evalúe las solicitudes de manera centralizada.

## Arquitectura del Sistema

### Participantes del Proceso (Lanes BPMN)

| Lane | Responsabilidad |
|------|-----------------|
| **Empleado** | Inicia el proceso, envía datos del proveedor, recibe notificaciones |
| **ChatBot Telegram** | Recibe datos, valida información, deriva a Compras, registra proveedores aprobados |
| **Departamento de Compras** | Evalúa proveedores, aprueba o rechaza solicitudes |

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO TELEGRAM                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Empleado   │  │  ChatBot     │  │  Depto. Compras       │   │
│  │              │──│  Telegram    │──│                      │   │
│  │              │  │              │  │                      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   ARCHIVOS CSV      │
                 │  - usuarios.csv     │
                 │  - solicitudes.csv  │
                 │  - proveedores.csv  │
                 └─────────────────────┘
```

### Estructura del Proyecto

```
bot_proveedores/
├── main.py                 # Punto de entrada del bot
├── config.py               # Configuración global
├── database/
│   ├── db.py               # Gestión de archivos CSV
│   └── models.py           # Modelos de datos
├── bot/
│   ├── handlers.py         # Manejadores de comandos y mensajes
│   ├── states.py           # Definición de estados
│   └── validators.py       # Validadores de datos
├── services/
│   ├── proveedor_service.py # Lógica de negocio de proveedores
│   └── compras_service.py    # Lógica del departamento de compras
├── data/
│   ├── usuarios.csv        # Usuarios y estados
│   ├── solicitudes_proveedor.csv  # Solicitudes pendientes
│   └── proveedores.csv     # Proveedores registrados
└── requirements.txt        # Dependencias
```

## Estados del Chatbot

| Estado | Descripción |
|--------|-------------|
| `INICIO` | Esperando comando /start |
| `REGISTRANDO_RAZON_SOCIAL` | Solicitando razón social |
| `REGISTRANDO_CUIT` | Solicitando CUIT |
| `REGISTRANDO_CONTACTO` | Solicitando nombre de contacto |
| `REGISTRANDO_TELEFONO` | Solicitando teléfono |
| `REGISTRANDO_EMAIL` | Solicitando email |
| `REGISTRANDO_DIRECCION` | Solicitando dirección |
| `REGISTRANDO_RUBRO` | Solicitando rubro |
| `REGISTRANDO_DESCRIPCION` | Solicitando descripción |
| `VALIDANDO_DATOS` | Validando información ingresada |
| `ESPERANDO_APROBACION` | Solicitud enviada a Compras |
| `FINALIZADO` | Proceso completado |

## Estados de Solicitud

| Estado | Descripción |
|--------|-------------|
| `BORRADOR` | Datos cargados, aún no enviados |
| `PENDIENTE_REVISION` | Enviada a Departamento de Compras |
| `APROBADO` | Solicitud aprobada, proveedor registrado |
| `RECHAZADO` | Solicitud rechazada |

## Instalación

### Requisitos Previos

- Python 3.8+
- Token de bot de Telegram (obtenido de @BotFather)

### Pasos

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar el token del bot**
Editar `config.py` y colocar el token de Telegram:
```python
TELEGRAM_TOKEN = "TU_TOKEN_AQUI"
```

5. **Inicializar estructura de datos**
```bash
python main.py --init
```

## Ejecución

```bash
python main.py
```

El bot estará activo y responderá a los comandos en Telegram.

## Comandos Disponibles

### Para Empleados

| Comando | Descripción |
|---------|-------------|
| `/start` | Inicia el proceso de registro de proveedor |
| `/cancelar` | Cancela la operación actual y limpia el estado |
| `/ayuda` | Muestra la lista de comandos disponibles |
| `/estado` | Muestra el estado actual del proceso |

### Para Departamento de Compras

| Comando | Descripción |
|---------|-------------|
| `/solicitudes` | Lista todas las solicitudes pendientes |
| `/aprobar <id>` | Aprueba la solicitud con el ID especificado |
| `/rechazar <id>` | Rechaza la solicitud con el ID especificado |
| `/solicitud <id>` | Muestra el detalle de una solicitud |

## Flujo del Proceso

### Camino Exitoso

1. Empleado ejecuta `/start`
2. Bot solicita datos del proveedor (razón social, CUIT, contacto, teléfono, email, dirección, rubro, descripción)
3. Bot valida cada campo
4. Si datos incompletos o inválidos, solicita corrección
5. Bot envía solicitud a Departamento de Compras con estado `PENDIENTE_REVISION`
6. Compras ejecuta `/aprobar <id>`
7. Bot registra proveedor en base de datos
8. Bot notifica al empleado: "Proveedor aprobado y registrado correctamente"

### Camino de Rechazo

1. (Pasos 1-5 iguales al camino exitoso)
6. Compras ejecuta `/rechazar <id>`
7. Bot actualiza estado a `RECHAZADO`
8. Bot notifica al empleado: "Solicitud rechazada"

## Persistencia de Datos

El sistema utiliza archivos CSV como simulación de base de datos:

- **`data/usuarios.csv`**: Almacena usuarios de Telegram y sus estados
- **`data/solicitudes_proveedor.csv`**: Solicitudes enviadas a Compras
- **`data/proveedores.csv`**: Proveedores definitivamente registrados

Esta estructura permite migrar a una base de datos SQL sin modificar la lógica principal.

## Validaciones Implementadas

- **CUIT**: Solo números, 11 dígitos
- **Email**: Formato válido con @ y dominio
- **Teléfono**: Solo números, entre 8 y 15 dígitos
- **Campos obligatorios**: Ningún campo puede estar vacío

## Licencia

Proyecto académico - UTN
