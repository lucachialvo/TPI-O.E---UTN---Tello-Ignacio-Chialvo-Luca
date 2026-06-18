# Manual de Usuario - Bot de Alta de Proveedores

## Introducción

Este chatbot de Telegram automatiza el proceso de registro de nuevos proveedores en la empresa. El sistema sigue el flujo BPMN definido, interactuando con el empleado y el Departamento de Compras.

## Requisitos Previos

- Tener instalado Telegram en el dispositivo
- Contar con un token de acceso proporcionado por el administrador

---

## Comandos para Empleados

### `/start`

**Descripción**: Inicia el proceso de registro de un nuevo proveedor.

**Uso**:
1. Escribir `/start` en el chat del bot
2. El bot mostrará un mensaje de bienvenida explicando el proceso
3. El bot comenzará a solicitar los datos del proveedor

**Flujo**:
```
Bot: "¡Bienvenido al sistema de registro de proveedores!"
Bot: "Me ajudaré a registrar un nuevo proveedor. Comenzaremos con los datos."
Bot: "Ingrese la RAZÓN SOCIAL del proveedor:"
```

---

### `/cancelar`

**Descripción**: Cancela la operación actual y limpia el estado del usuario.

**Uso**:
1. Escribir `/cancelar` en cualquier momento durante el registro
2. El bot cancelará el proceso y limpiará los datos ingresados
3. El usuario quedará en estado inicial

**Nota**: Si se cancela, los datos ya ingresados se perderán y deberá comenzar desde cero.

---

### `/ayuda`

**Descripción**: Muestra la lista de comandos disponibles y una breve descripción.

**Uso**:
1. Escribir `/ayuda` en el chat del bot
2. El bot mostrará una lista con todos los comandos

---

### `/estado`

**Descripción**: Muestra el estado actual del proceso de registro.

**Uso**:
1. Escribir `/estado` en el chat del bot
2. El bot mostrará en qué paso del proceso se encuentra

---

## Flujo Completo de Registro (Empleado)

### Paso 1: Inicio
```
Usuario: /start
Bot: Bienvenido al sistema de registro de proveedores.
     Este bot le ayudará a registrar un nuevo proveedor en nuestra base de datos.
     Comenzaremos solicitando los datos del proveedor.
```

### Paso 2: Captura de Datos
El bot solicitará cada dato en orden:

| Orden | Campo | Descripción | Ejemplo |
|-------|-------|-------------|---------|
| 1 | Razón Social | Nombre legal de la empresa | "Acme S.A." |
| 2 | CUIT | Clave Única de Identificación Tributaria | "30712345678" |
| 3 | Contacto | Nombre del responsable | "Juan Pérez" |
| 4 | Teléfono | Número de contacto | "1122334455" |
| 5 | Email | Correo electrónico | "juan@empresa.com" |
| 6 | Dirección | Domicilio fiscal | "Av. Corrientes 1234, CABA" |
| 7 | Rubro | Actividad comercial | "Tecnología" |
| 8 | Descripción | Productos o servicios | "Proveedor de software" |

### Paso 3: Validación
```
Bot: Validando información...
     ✓ Razón Social: Completo
     ✓ CUIT: Completo
     ✓ Email: Formato válido
     ...
```

### Paso 4: Datos Incompletos o Inválidos
Si algún dato falta o es inválido:

```
Bot: El correo ingresado no tiene formato válido.
     Por favor, ingrese un correo electrónico válido.
     Ejemplo: ejemplo@empresa.com
Usuario: juan@empresa.com
Bot: ✓ Email válido.
```

### Paso 5: Envío a Compras
Una vez validados todos los datos:

```
Bot: Todos los datos han sido validados correctamente.
     Su solicitud ha sido enviada al Departamento de Compras para evaluación.
     Usted recibirá una notificación cuando el proceso finalice.
     Estado: PENDIENTE_REVISION
```

### Paso 6: Notificación Final

**Si es aprobado:**
```
Bot: ✓ Su proveedor fue aprobado y registrado correctamente.
     Proveedor: Acme S.A.
     CUIT: 30712345678
```

**Si es rechazado:**
```
Bot: ✗ La solicitud del proveedor fue rechazada.
     Proveedor: Acme S.A.
     Para más información, contacte al Departamento de Compras.
```

---

## Comandos para Departamento de Compras

### `/solicitudes`

**Descripción**: Lista todas las solicitudes pendientes de revisión.

**Uso**:
1. Escribir `/solicitudes` en el chat del bot
2. El bot mostrará una lista de solicitudes pendientes

**Formato de respuesta**:
```
Solicitudes Pendientes:

#1 - Empresa XYZ
  Razón Social: Empresa XYZ S.A.
  CUIT: 30712345678
  Estado: Pendiente revisión
  Fecha: 2026-01-15 10:30:00

#2 - Proveedor ABC
  Razón Social: Proveedor ABC Ltda.
  CUIT: 30123456789
  Estado: Pendiente revisión
  Fecha: 2026-01-15 11:00:00
```

---

### `/aprobar <id>`

**Descripción**: Aprueba la solicitud de alta con el ID especificado.

**Uso**:
1. Escribir `/aprobar 15` (reemplazando 15 por el ID de la solicitud)
2. El bot aprobará la solicitud
3. El proveedor será registrado en la base de datos
4. Se notificará al empleado

**Ejemplo**:
```
Usuario (Compras): /aprobar 15
Bot: ✓ Solicitud #15 aprobada.
     El proveedor "Empresa XYZ S.A." ha sido registrado.
     Se ha notificado al empleado.
```

---

### `/rechazar <id>`

**Descripción**: Rechaza la solicitud de alta con el ID especificado.

**Uso**:
1. Escribir `/rechazar 15` (reemplazando 15 por el ID de la solicitud)
2. El bot rechazará la solicitud
3. El proveedor NO será registrado
4. Se notificará al empleado

**Ejemplo**:
```
Usuario (Compras): /rechazar 15
Bot: ✗ Solicitud #15 rechazada.
     El proveedor "Empresa XYZ S.A." no ha sido registrado.
     Se ha notificado al empleado.
```

---

### `/solicitud <id>`

**Descripción**: Muestra el detalle completo de una solicitud específica.

**Uso**:
1. Escribir `/solicitud 15` (reemplazando 15 por el ID de la solicitud)
2. El bot mostrará todos los datos de la solicitud

**Formato de respuesta**:
```
Solicitud #15

Razón Social: Empresa XYZ S.A.
CUIT: 30712345678
Contacto: Ana López
Teléfono: 1122334455
Email: ana@empresa.com
Dirección: CABA 123
Rubro: Servicios
Descripción: Proveedor tecnológico
Estado: PENDIENTE_REVISION
Fecha de creación: 2026-01-15 10:30:00
Solicitante (Telegram ID): 123456789
```

---

## Códigos de Estado

| Código | Significado |
|--------|-------------|
| `INICIO` | Sin proceso activo |
| `REGISTRANDO_*` | En proceso de captura de datos |
| `VALIDANDO_DATOS` | Verificando información |
| `ESPERANDO_APROBACION` | En espera de decisión de Compras |
| `FINALIZADO` | Proceso completado exitosamente |
| `CANCELADO` | Proceso cancelado por el usuario |

---

## Estados de Solicitud

| Estado | Significado |
|--------|-------------|
| `BORRADOR` | Cargado pero no enviado |
| `PENDIENTE_REVISION` | Esperando evaluación de Compras |
| `APROBADO` | Aprobado, proveedor registrado |
| `RECHAZADO` | Rechazado, no se registró |

---

## Ejemplos de Interacción

### Ejemplo 1: Registro Exitoso

```
Usuario: /start
Bot: Bienvenido al sistema de registro de proveedores.
Bot: Ingrese la RAZÓN SOCIAL del proveedor:
Usuario: Acme Argentina S.A.
Bot: ✓ Razón Social registrada.
Bot: Ingrese el CUIT del proveedor (solo números, 11 dígitos):
Usuario: 30712345678
Bot: ✓ CUIT registrado.
Bot: Ingrese el NOMBRE del contacto:
Usuario: Juan Pérez
Bot: ✓ Contacto registrado.
Bot: Ingrese el TELÉFONO de contacto:
Usuario: 1122334455
Bot: ✓ Teléfono registrado.
Bot: Ingrese el EMAIL del proveedor:
Usuario: juan@acme.com
Bot: ✓ Email registrado.
Bot: Ingrese la DIRECCIÓN:
Usuario: Av. Libertador 5000, CABA
Bot: ✓ Dirección registrada.
Bot: Ingrese el RUBRO:
Usuario: Tecnología
Bot: ✓ Rubro registrado.
Bot: Ingrese una DESCRIPCIÓN del producto/servicio:
Usuario: Venta y soporte de software empresarial
Bot: ✓ Descripción registrada.
Bot: Todos los datos han sido validados.
Bot: Solicitud enviada al Departamento de Compras.
Bot: Estado: PENDIENTE_REVISION
[Después, Compras ejecuta /aprobar 1]
Bot: ✓ Su proveedor fue aprobado y registrado correctamente.
```

### Ejemplo 2: Corrección de Datos

```
Bot: Ingrese el EMAIL del proveedor:
Usuario: juan@
Bot: El correo ingresado no tiene formato válido.
Bot: Por favor, ingrese un correo electrónico válido.
Bot: Ejemplo: ejemplo@empresa.com
Usuario: juan@empresa.com
Bot: ✓ Email válido registrado.
```

### Ejemplo 3: Cancelación

```
Usuario: /cancelar
Bot: Operación cancelada.
Bot: Los datos ingresados han sido eliminados.
Bot: Use /start para iniciar un nuevo registro.
```

---

## Manejo de Errores

| Situación | Respuesta del Bot |
|-----------|-------------------|
| Campo vacío | "Este campo es obligatorio. Ingrese un valor." |
| CUIT con letras | "El CUIT debe contener solo números." |
| Email sin @ | "El correo debe contener el símbolo @" |
| Comando desconocido | "No entiendo el comando. Use /ayuda para ver opciones." |
| Solicitud inexistente | "No se encontró la solicitud #X." |

---

## Contacto y Soporte

Para consultas sobre el sistema, contactar al administrador del bot.
