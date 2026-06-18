# Diccionario de Datos

## Entidades y Relaciones

```
┌──────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│    Usuarios      │     │ SolicitudesProveedor │     │   Proveedores    │
├──────────────────┤     ├──────────────────────┤     ├──────────────────┤
│ telegram_id (PK) │────▶│ telegram_usuario (FK) │     │ id (PK)          │
│ nombre           │     │ id (PK)               │     │ razon_social      │
│ estado_actual    │     │ razon_social          │     │ cuit (UNIQUE)     │
│ fecha_inicio     │     │ cuit                  │     │ contacto          │
└──────────────────┘     │ contacto             │     │ telefono          │
                         │ telefono            │     │ email             │
                         │ email                │     │ direccion         │
                         │ direccion            │     │ rubro             │
                         │ rubro                │     │ descripcion       │
                         │ descripcion          │     │ fecha_alta        │
                         │ estado               │     └──────────────────┘
                         │ fecha_creacion       │
                         └──────────────────────┘
```

---

## Archivo: usuarios.csv

### Descripción
Almacena los usuarios de Telegram que interactúan con el bot y el estado actual de su conversación.

### Campos

| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| `id` | INTEGER | Identificador único del registro | PRIMARY KEY, AUTOINCREMENT |
| `telegram_id` | INTEGER | ID único del usuario de Telegram | NOT NULL, UNIQUE |
| `nombre` | TEXT | Nombre del usuario | NULL si no se proporcionó |
| `estado_actual` | TEXT | Estado actual en la máquina de estados | NOT NULL, DEFAULT 'INICIO' |
| `fecha_inicio` | TEXT | Fecha y hora del primer contacto | FORMATO: YYYY-MM-DD HH:MM:SS |

### Estados Posibles (estado_actual)

| Estado | Descripción |
|--------|-------------|
| `INICIO` | Usuario acaba de iniciar |
| `REGISTRANDO_RAZON_SOCIAL` | Solicitando razón social |
| `REGISTRANDO_CUIT` | Solicitando CUIT |
| `REGISTRANDO_CONTACTO` | Solicitando contacto |
| `REGISTRANDO_TELEFONO` | Solicitando teléfono |
| `REGISTRANDO_EMAIL` | Solicitando email |
| `REGISTRANDO_DIRECCION` | Solicitando dirección |
| `REGISTRANDO_RUBRO` | Solicitando rubro |
| `REGISTRANDO_DESCRIPCION` | Solicitando descripción |
| `VALIDANDO_DATOS` | En proceso de validación |
| `ESPERANDO_APROBACION` | Esperando respuesta de Compras |
| `FINALIZADO` | Proceso completado |
| `CANCELADO` | Usuario canceló la operación |

### Ejemplo de Registro

```csv
id,telegram_id,nombre,estado_actual,fecha_inicio
1,123456789,Juan Perez,REGISTRANDO_EMAIL,2026-01-15 10:30:00
```

---

## Archivo: solicitudes_proveedor.csv

### Descripción
Almacena las solicitudes de alta de proveedores enviadas al Departamento de Compras para evaluación.

### Campos

| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| `id` | INTEGER | Identificador único de solicitud | PRIMARY KEY, AUTOINCREMENT |
| `telegram_usuario` | INTEGER | ID del usuario Telegram que creó la solicitud | FK → usuarios.telegram_id |
| `razon_social` | TEXT | Nombre legal de la empresa | NOT NULL |
| `cuit` | TEXT | Clave Única de Identificación Tributaria | NOT NULL, 11 dígitos |
| `contacto` | TEXT | Nombre de la persona de contacto | NOT NULL |
| `telefono` | TEXT | Número de teléfono de contacto | NOT NULL |
| `email` | TEXT | Correo electrónico | NOT NULL, formato válido |
| `direccion` | TEXT | Dirección fiscal | NOT NULL |
| `rubro` | TEXT | Rubro o industria del proveedor | NOT NULL |
| `descripcion` | TEXT | Descripción de productos/servicios | NOT NULL |
| `estado` | TEXT | Estado actual de la solicitud | NOT NULL |
| `fecha_creacion` | TEXT | Fecha y hora de creación | FORMATO: YYYY-MM-DD HH:MM:SS |

### Estados Posibles (estado)

| Estado | Descripción | Transiciones válidas |
|--------|-------------|---------------------|
| `BORRADOR` | Datos cargados, no enviados | → PENDIENTE_REVISION |
| `PENDIENTE_REVISION` | Enviada a Compras | → APROBADO, RECHAZADO |
| `APROBADO` | Aprobada por Compras | (estado final) |
| `RECHAZADO` | Rechazada por Compras | (estado final) |

### Ejemplo de Registro

```csv
id,telegram_usuario,razon_social,cuit,contacto,telefono,email,direccion,rubro,descripcion,estado,fecha_creacion
1,123456789,Empresa XYZ S.A.,30712345678,Ana Lopez,1122334455,ana@empresa.com,CABA 123,Servicios,Proveedor tecnológico,PENDIENTE_REVISION,2026-01-15 10:35:00
```

---

## Archivo: proveedores.csv

### Descripción
Base de datos final de proveedores registrados. Solo contiene proveedores APPROBADOS por el Departamento de Compras.

### Campos

| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| `id` | INTEGER | Identificador único del proveedor | PRIMARY KEY, AUTOINCREMENT |
| `razon_social` | TEXT | Nombre legal de la empresa | NOT NULL |
| `cuit` | TEXT | CUIT del proveedor | NOT NULL, UNIQUE |
| `contacto` | TEXT | Nombre del contacto | NOT NULL |
| `telefono` | TEXT | Teléfono de contacto | NOT NULL |
| `email` | TEXT | Correo electrónico | NOT NULL |
| `direccion` | TEXT | Dirección fiscal | NOT NULL |
| `rubro` | TEXT | Rubro comercial | NOT NULL |
| `descripcion` | TEXT | Descripción de productos/servicios | NOT NULL |
| `fecha_alta` | TEXT | Fecha de registro en el sistema | FORMATO: YYYY-MM-DD HH:MM:SS |

### Regla de Negocio
Un proveedor NO puede estar duplicado por CUIT. Antes de registrar un proveedor aprobado, se debe verificar que no exista otro con el mismo CUIT.

### Ejemplo de Registro

```csv
id,razon_social,cuit,contacto,telefono,email,direccion,rubro,descripcion,fecha_alta
1,Empresa XYZ S.A.,30712345678,Ana Lopez,1122334455,ana@empresa.com,CABA 123,Servicios,Proveedor tecnológico,2026-01-15 11:00:00
```

---

## Validaciones de Datos

### CUIT (Argentina)
- Solo caracteres numéricos
- Exactamente 11 dígitos
- Formato: XX-XXXXXXXX-X (con o sin guiones, se normaliza)

### Email
- Debe contener exactamente un @
- Debe tener al menos un carácter antes del @
- Debe tener al menos un punto después del @ (dominio)
- No puede empezar o terminar con @

### Teléfono
- Solo caracteres numéricos
- Entre 8 y 15 dígitos
- Puede incluir + al inicio (código de país)

### Campos Obligatorios
Todos los campos son obligatorios y no pueden estar vacíos ni ser solo espacios en blanco.

---

## Reglas de Persistencia

1. **Crear registro**: Generar nuevo ID autoincremental
2. **Leer solicitudes pendientes**: Filtrar por estado = 'PENDIENTE_REVISION'
3. **Actualizar estado**: Modificar solo el campo estado y fecha
4. **Buscar proveedor existente**: Filtrar por CUIT en proveedores.csv
5. **Evitar duplicados**: Verificar CUIT único antes de insertar en proveedores.csv
6. **Recuperación ante reinicio**: Los archivos CSV mantienen los datos sin necesidad de base de datos
