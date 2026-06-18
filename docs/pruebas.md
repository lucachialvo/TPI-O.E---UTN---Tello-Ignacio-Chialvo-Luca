# Documento de Pruebas - Bot de Alta de Proveedores

## Resumen

Este documento contiene los casos de prueba diseñados para verificar el correcto funcionamiento del chatbot de Telegram para alta de proveedores.

---

## Caso de Prueba 1: Registro Exitoso (CP-001)

### Objetivo
Verificar que el flujo completo de registro de un proveedor funciona correctamente cuando el empleado ingresa todos los datos válidos.

### Precondiciones
- Bot activo y accesible
- Usuario de Telegram sin proceso activo

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Usuario envía `/start` | Bot responde con mensaje de bienvenida |
| 2 | Bot solicita "Razón Social" | Usuario ingresa "Tech Solutions S.A." |
| 3 | Bot solicita "CUIT" | Usuario ingresa "30712345678" |
| 4 | Bot solicita "Contacto" | Usuario ingresa "María García" |
| 5 | Bot solicita "Teléfono" | Usuario ingresa "1122334455" |
| 6 | Bot solicita "Email" | Usuario ingresa "maria@techsolutions.com" |
| 7 | Bot solicita "Dirección" | Usuario ingresa "Av. Santa Fe 1234, CABA" |
| 8 | Bot solicita "Rubro" | Usuario ingresa "Tecnología" |
| 9 | Bot solicita "Descripción" | Usuario ingresa "Desarrollo de software" |
| 10 | Bot valida y envía a Compras | Estado cambia a PENDIENTE_REVISION |
| 11 | Compras ejecuta `/aprobar <id>` | Proveedor registrado, empleado notificado |

### Resultado Esperado
- Proveedor registrado en `proveedores.csv`
- Solicitud actualizada a estado `APROBADO`
- Empleado recibe mensaje: "Su proveedor fue aprobado y registrado correctamente"

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 2: Datos Incompletos - Falta Email (CP-002)

### Objetivo
Verificar que el sistema detecta y solicita campos obligatorios faltantes.

### Precondiciones
- Bot activo
- Usuario en proceso de registro

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Usuario completa pasos 1-5 (hasta Email) | Datos registrados correctamente |
| 2 | Bot solicita "Email" | Usuario envía texto vacío o "-" |
| 3 | Sistema detecta campo vacío | Bot indica: "Este campo es obligatorio" |
| 4 | Bot re-solicita "Email" | Usuario ingresa "info@empresa.com" |
| 5 | Sistema valida email | Bot acepta y continúa al siguiente campo |

### Resultado Esperado
- Sistema no permite avanzar sin completar campos obligatorios
- Solo se solicita el campo faltante, no todos los datos nuevamente

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 3: Formato Inválido de CUIT (CP-003)

### Objetivo
Verificar que el sistema valida el formato del CUIT y rechaza datos incorrectos.

### Precondiciones
- Bot activo
- Usuario en proceso de registro

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Bot solicita "CUIT" | Usuario ingresa "abc123" |
| 2 | Sistema detecta formato inválido | Bot indica: "El CUIT debe contener solo números" |
| 3 | Bot re-solicita "CUIT" | Usuario ingresa "30712345678" |
| 4 | Sistema valida CUIT | Bot acepta (11 dígitos numéricos) |

### Resultado Esperado
- Sistema rechaza CUIT no numérico
- Sistema acepta CUIT válido de 11 dígitos

### Resultado Esperado (CUIT con formato incorrecto)
| Entrada | Resultado Esperado |
|---------|-------------------|
| "abc123" | Rechazo: "solo números" |
| "12345" | Rechazo: "debe tener 11 dígitos" |
| "30712345678" | Aceptado |
| "30-71234567-8" | Aceptado (normalizado internamente) |

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 4: Email con Formato Inválido (CP-004)

### Objetivo
Verificar que el sistema valida el formato del email.

### Precondiciones
- Bot activo
- Usuario en proceso de registro

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Bot solicita "Email" | Usuario ingresa "juan@" |
| 2 | Sistema detecta formato inválido | Bot indica formato inválido |
| 3 | Bot muestra ejemplo | Ejemplo: "ejemplo@empresa.com" |
| 4 | Usuario re-ingresa email | Usuario ingresa "juan@empresa.com" |
| 5 | Sistema valida email | Bot acepta email |

### Casos de Email a Probar

| Email | Resultado Esperado |
|-------|-------------------|
| "juan@" | Rechazo: falta dominio |
| "@empresa.com" | Rechazo: falta usuario |
| "juan@empresa" | Rechazo: falta TLD |
| "juan@empresa.com" | Aceptado |
| "juan.carlos@empresa.com" | Aceptado |

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 5: Rechazo de Solicitud por Compras (CP-005)

### Objetivo
Verificar el flujo completo cuando el Departamento de Compras rechaza una solicitud.

### Precondiciones
- Bot activo
- Solicitud en estado PENDIENTE_REVISION

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Solicitud creada con estado PENDIENTE_REVISION | ID de solicitud = 5 |
| 2 | Compras ejecuta `/rechazar 5` | Bot responde con confirmación |
| 3 | Estado de solicitud actualizado | Estado = RECHAZADO |
| 4 | Empleado notificado | Mensaje: "La solicitud fue rechazada" |
| 5 | Verificar proveedores.csv | El proveedor NO debe estar registrado |

### Resultado Esperado
- Solicitud con estado actualizado a RECHAZADO
- Proveedor NO existe en proveedores.csv
- Empleado recibe notificación de rechazo

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 6: Cancelación de Proceso (CP-006)

### Objetivo
Verificar que el comando `/cancelar` limpia correctamente el estado del usuario.

### Precondiciones
- Bot activo
- Usuario con proceso activo (datos parcialmente cargados)

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Usuario ha completado 3 campos | Estado: REGISTRANDO_TELEFONO |
| 2 | Usuario envía `/cancelar` | Bot responde con confirmación |
| 3 | Estado del usuario limpiado | Estado: CANCELADO o INICIO |
| 4 | Datos temporales eliminados | No se guarda nada en CSV |
| 5 | Usuario puede iniciar nuevo proceso | `/start` funciona correctamente |

### Resultado Esperado
- Estado limpiado a INICIO/CANCELADO
- Datos parciales no persiste
- Nuevo registro puede comenzar

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 7: Comando Inválido (CP-007)

### Objetivo
Verificar que el sistema responde correctamente a comandos desconocidos.

### Precondiciones
- Bot activo
- Usuario en cualquier estado

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Usuario envía "/comandoinexistente" | Bot responde con mensaje de error |
| 2 | Mensaje sugiere usar /ayuda | "No entiendo. Use /ayuda para ver comandos." |

### Resultado Esperado
- Bot responde con mensaje amigable
- No se corrompe el estado del usuario
- Invita a usar /ayuda

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 8: Listar Solicitudes Pendientes (CP-008)

### Objetivo
Verificar que el comando `/solicitudes` muestra correctamente las solicitudes pendientes.

### Precondiciones
- Bot activo
- Al menos 2 solicitudes en estado PENDIENTE_REVISION

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Compras ejecuta `/solicitudes` | Bot muestra lista de solicitudes |
| 2 | Verificar formato | Muestra ID, Razón Social, Estado, Fecha |
| 3 | Verificar contenido | Lista solo solicitudes PENDIENTE_REVISION |

### Resultado Esperado
```
Solicitudes Pendientes:

#1 - Empresa XYZ
  Razón Social: Empresa XYZ S.A.
  Estado: Pendiente revisión
  Fecha: 2026-01-15 10:30:00

#2 - Proveedor ABC
  Razón Social: Proveedor ABC Ltda.
  Estado: Pendiente revisión
  Fecha: 2026-01-15 11:00:00
```

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 9: Aprobación de Solicitud Específica (CP-009)

### Objetivo
Verificar que se puede aprobar una solicitud específica sin afectar otras.

### Precondiciones
- Bot activo
- 3 solicitudes pendientes (IDs 10, 11, 12)

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Compras ejecuta `/aprobar 11` | Solo solicitud #11 se aprueba |
| 2 | Verificar #10 y #12 | Continúan en PENDIENTE_REVISION |
| 3 | Verificar #11 | Estado = APROBADO, en proveedores.csv |
| 4 | Ejecutar `/solicitudes` | #10 y #12 listadas, #11 no aparece |

### Resultado Esperado
- Solo se procesa la solicitud especificada
- Las demás solicitudes permanecen intactas

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Caso de Prueba 10: Intento de Duplicar Proveedor (CP-010)

### Objetivo
Verificar que el sistema impide registrar proveedores con CUIT duplicado.

### Precondiciones
- Bot activo
- Proveedor existente con CUIT "30712345678"

### Pasos a Ejecutar

| Paso | Acción | Resultado Esperado |
|------|--------|-------------------|
| 1 | Nuevo usuario inicia `/start` | Proceso de registro normal |
| 2 | Completa todos los campos | Ingresa CUIT: "30712345678" (existente) |
| 3 | Compras ejecuta `/aprobar <id>` | Sistema detecta CUIT duplicado |

### Resultado Esperado
- El sistema detecta CUIT existente
- Mensaje de error impide registro duplicado
- El proveedor NO se registra

### Resultado Real
□ Cumple  □ Parcial  □ Fallido

### Observaciones
_________________________________

---

## Pruebas de Estrés

### PE-01: Múltiples Usuarios Simultáneos

**Objetivo**: Verificar que el bot maneja correctamente múltiples usuarios registrando proveedores concurrentemente.

**Simulación**:
1. Usuario A inicia `/start`
2. Usuario B inicia `/start`
3. Usuario C inicia `/start`
4. Los tres completan registros
5. Compras aprueba las 3 solicitudes

**Criterio de Éxito**:
- Cada usuario mantiene su propio estado independiente
- Los datos no se mezclan entre usuarios
- Las 3 solicitudes se crean correctamente

---

### PE-02: Mensajes Fuera de Orden

**Objetivo**: Verificar la robustez del bot ante mensajes fuera del orden esperado.

**Simulación**:
1. Usuario inicia `/start`
2. Bot solicita Razón Social
3. Usuario envía `/ayuda` en lugar de la razón social
4. Bot responde con ayuda pero mantiene el estado
5. Usuario luego envía la razón social
6. Proceso continúa normalmente

**Criterio de Éxito**:
- El bot no se "rompe" con comandos inesperados durante el flujo
- Mantiene el estado correcto del usuario
- Permite continuar el registro después de interrumpir

---

### PE-03: Datos Incorrectos Repetidos

**Objetivo**: Verificar que el bot maneja correctamente errores consecutivos del usuario.

**Simulación**:
1. Usuario intenta registrar email inválido 3 veces seguidas
2. Bot rechaza cada intento con mensaje de error
3. Usuario finalmente ingresa email válido
4. Proceso continúa normalmente

**Criterio de Éxito**:
- El bot no entra en loop infinito
- Mantiene el estado de registro
- Acepta datos válidos después de múltiples intentos fallidos

---

### PE-04: Reinicio del Bot con Datos Persistidos

**Objetivo**: Verificar que los datos persisten ante un reinicio del bot.

**Simulación**:
1. Usuario inicia `/start` y completa 5 campos
2. Se detiene el proceso del bot (Ctrl+C)
3. Se reinicia el bot
4. Usuario verifica su estado con `/estado`

**Criterio de Éxito**:
- El estado del usuario se mantiene (datos en CSV)
- El usuario puede continuar desde donde dejó
- No se pierden datos intermedios

---

## Resumen de Resultados

| Caso | Descripción | Estado |
|------|-------------|--------|
| CP-001 | Registro exitoso | □ |
| CP-002 | Datos incompletos | □ |
| CP-003 | CUIT inválido | □ |
| CP-004 | Email inválido | □ |
| CP-005 | Rechazo por Compras | □ |
| CP-006 | Cancelación | □ |
| CP-007 | Comando inválido | □ |
| CP-008 | Listar solicitudes | □ |
| CP-009 | Aprobación específica | □ |
| CP-010 | Proveedor duplicado | □ |

**Leyenda**: □ Pendiente  ● Aprobado  ✗ Fallido

---

## Firmas

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Responsable de Pruebas | | | |
| Validación | | | |
