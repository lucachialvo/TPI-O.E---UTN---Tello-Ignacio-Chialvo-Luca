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

## Instrucciones para la puesta en funcionamiento

### Configuración inicial

Una vez clonado el repositorio, es necesario configurar el archivo de configuración:

```bash
cp bot_proveedores/config.example.py bot_proveedores/config.py
```

> **Nota**: `config.py` contiene el token de Telegram y no está incluido en el repositorio por seguridad.

### Ejecución

Para poner en funcionamiento el programa, es necesario acceder mediante la terminal al directorio del proyecto utilizando el comando:
```
cd bot_proveedores
```
Una vez ubicado dentro del directorio correspondiente, se deben instalar las dependencias necesarias para la ejecución del sistema. En particular, se requiere la librería python-telegram-bot en su versión 20.7, la cual puede instalarse mediante el siguiente comando:
```
pip install python-telegram-bot==20.7
```
Antes de ejecutar el programa, es necesario configurar el token de autenticación del bot de Telegram. Este token permite que la aplicación pueda comunicarse con la API de Telegram y gestionar la recepción y envío de mensajes.

Para obtener un token válido, el usuario debe ingresar a la aplicación de Telegram y buscar el bot oficial denominado BotFather. Desde este bot se debe crear un nuevo bot utilizando el comando correspondiente, asignándole un nombre y un identificador único. Una vez finalizado el proceso de creación, BotFather proporcionará un token de acceso que deberá ser utilizado para configurar la aplicación.

El token obtenido debe establecerse como una variable de entorno antes de iniciar la ejecución del programa. Para ello, se debe ejecutar el siguiente comando en la terminal:
```
export TELEGRAM_TOKEN="su_token_aqui"
```

Como alternativa, para evitar configurar la variable manualmente cada vez que se inicia una nueva sesión de terminal, se puede agregar esta línea al archivo de configuración del intérprete de comandos utilizado:

Para usuarios de Zsh:
```
~/.zshrc
```
Para usuarios de Bash:
```
~/.bashrc
```

El programa obtiene el valor de esta variable desde el archivo config.py mediante la siguiente instrucción:
```python
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
```
De esta forma, el token de acceso permanece separado del código fuente, mejorando la seguridad y facilitando la configuración del sistema en diferentes entornos de ejecución.

Finalmente, luego de instalar las dependencias y configurar correctamente la variable de entorno, el programa puede ejecutarse mediante:
```
python main.py
```
o, dependiendo de la configuración del sistema:
```
python3 main.py
```

Al iniciar la ejecución del archivo principal, el bot quedará operativo y preparado para recibir y procesar mensajes correctamente.

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
