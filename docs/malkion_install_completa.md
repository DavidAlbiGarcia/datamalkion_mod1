---
title: Instalación
---

# Instalación del sistema Malkion

## URLS

- [Repositorio](https://github.com/DavidAlbiGarcia/malkion) https://github.com/DavidAlbiGarcia/malkion
- [GitHubPages](https://davidalbigarcia.github.io/malkion/) https://davidalbigarcia.github.io/malkion/

---

## Orden de instalación

Sigue este orden para instalar correctamente todos los módulos requeridos:

1. **Base** – se instala automáticamente con Odoo.
2. **Contacts** (`contacts`) – módulo de contactos de Odoo.
3. **Human Resources** (`hr`) – módulo de empleados.
4. **Malkion** – módulo personalizado de gestión de misiones y recursos.

Este orden garantiza que todas las dependencias estén disponibles al instalar `malkion`.


# Usuarios y contraseñas del sistema Malkion

## 👥 Usuarios base generados

Se han creado usuarios para cubrir todos los perfiles operativos y de gestión del sistema:

- **4 Arqueros**
- **4 Cazadores**
- **4 Recolectores**
- **1 Jefe de datos**
- **2 Gestores de equipo**
- **2 Gestores de hunters**
- **2 Gestores de transportes**
- **2 Conductores**
- **2 Empleados de Logística**
- **2 Empleados de Asclepios**
- **2 Vendedores**

**Formato de login:** `nombreRol` (por ejemplo: `mariaArquero`, `pepeCazador2`, etc.)  
**Contraseña común:** `potato`  
**Grupo base:** Todos pertenecen a `base.group_user`, además de su grupo específico de Malkion.

---

## 🔐 Logins, contraseñas y grupos

| Nombre                      | Login                   | Rol                  | Grupo Malkion         | Contraseña |
|----------------------------|--------------------------|----------------------|------------------------|------------|
| Maria Arquero              | `mariaArquero`           | Arquero              | `group_AGENTESCAMPO`   | potato     |
| Pepe Arquero               | `pepeArquero`            | Arquero              | `group_AGENTESCAMPO`   | potato     |
| Maria Arquero 2            | `mariaArquero2`          | Arquero              | `group_AGENTESCAMPO`   | potato     |
| Pepe Arquero 2             | `pepeArquero2`           | Arquero              | `group_AGENTESCAMPO`   | potato     |
| Pepe Cazador               | `pepeCazador`            | Cazador              | `group_AGENTESCAMPO`   | potato     |
| Maria Cazador              | `mariaCazador`           | Cazador              | `group_AGENTESCAMPO`   | potato     |
| Pepe Cazador 2             | `pepeCazador2`           | Cazador              | `group_AGENTESCAMPO`   | potato     |
| Maria Cazador 2            | `mariaCazador2`          | Cazador              | `group_AGENTESCAMPO`   | potato     |
| Maria Recolector           | `mariaRecolector`        | Recolector           | `group_AGENTESCAMPO`   | potato     |
| Pepe Recolector            | `pepeRecolector`         | Recolector           | `group_AGENTESCAMPO`   | potato     |
| Maria Recolector 2         | `mariaRecolector2`       | Recolector           | `group_AGENTESCAMPO`   | potato     |
| Pepe Recolector 2          | `pepeRecolector2`        | Recolector           | `group_AGENTESCAMPO`   | potato     |
| Pepe Conductor             | `pepeConductor`          | Conductor            | `group_AGENTESCAMPO`   | potato     |
| Maria Conductor            | `mariaConductor`         | Conductor            | `group_AGENTESCAMPO`   | potato     |
| Pepe Jefe de datos         | `pepeJefe_datos`         | Jefe de datos        | `group_MANAGER`        | potato     |
| Maria Gestor de equipo     | `mariaGestor_equipo`     | Gestor de equipo     | `group_MANAGER`        | potato     |
| Pepe Gestor de equipo      | `pepeGestor_equipo`      | Gestor de equipo     | `group_MANAGER`        | potato     |
| Pepe Gestor de hunters     | `pepeGestor_hunters`     | Gestor de hunters    | `group_MANAGER`        | potato     |
| Maria Gestor de hunters    | `mariaGestor_hunters`    | Gestor de hunters    | `group_MANAGER`        | potato     |
| Maria Gestor de transportes| `mariaGestor_transportes`| Gestor de transportes| `group_MANAGER`        | potato     |
| Pepe Gestor de transportes | `pepeGestor_transportes` | Gestor de transportes| `group_MANAGER`        | potato     |
| Asclepios 1                | `asclepios1`             | Asclepios            | `group_ASCLEPIOS`      | potato     |
| Asclepios 2                | `asclepios2`             | Asclepios            | `group_ASCLEPIOS`      | potato     |
| Logística 1                | `logistica1`             | Logística            | `group_LOGISTICA`      | potato     |
| Logística 2                | `logistica2`             | Logística            | `group_LOGISTICA`      | potato     |
| Ventas 1                   | `ventas1`                | Ventas               | `group_VENTAS`         | potato     |
| Ventas 2                   | `ventas2`                | Ventas               | `group_VENTAS`         | potato     |

> ✅ Los usuarios del grupo `group_MANAGER` tienen permisos completos sobre todos los modelos.



# Datos iniciales del sistema Malkion

## 🧤 Equipo

- **Guantes**, **Recipiente A** y **Traje**: 4 unidades cada uno.
- **Resto de tipos de equipo**: 2 unidades.
- **Medidor de gas**: 1 unidad.

**Distribución:**
- Todas las unidades están **repartidas entre los dos almacenes de equipo**.
- **Fecha de adquisición aleatoria** entre **2022 y 2024**.

- **Estado** : `disponible`.

---

## 🚚 Transporte

**Distribución entre almacenes:**

- `almacen_transporte_norte_valencia`: **9 transportes**
- `almacen_transporte_sur_valencia`: **9 transportes**
  - Reparto equitativo entre tipos

**Resumen de datos demo – Transportes:**

| Tipo de transporte | Cantidad |
|--------------------|----------|
| Coches             | 4        |
| Motos              | 4        |
| Furgonetas         | 4        |
| Camiones           | 4        |
| Otros              | 2 *(1 Quad rápido, 1 Remolque especial)* |

**Detalles adicionales:**

- **Campos definidos**: `name`, `matricula`, `tipo`, `estado`, `capacidad`, `fecha_adquisicion`, `fecha_itv`, `observaciones`, `almacen_id`
- **Estado**: Todos los transportes en `disponible`
- **Fecha de adquisición**: Entre **2018 y 2023**
- **Fecha ITV**: Hasta **2025**
- **Observaciones**: Descripciones breves según tipo (ej. *uso urbano*, *refrigeración*, *doble eje*, etc.)

---

## 📍 Puntos de Interés

**Resumen general:**

- **Entrega**: 3 puntos
- **Medición**: 11 puntos
- **Recogida**: 7 puntos  
→ **Total: 21 puntos**, todos ubicados en **Valencia**

**Listado detallado:**

### Entrega
- Punto Entrega 1 – Zona Entrega 1  
- Punto Entrega 2 – Zona Entrega 2  
- Punto Entrega 3 – Zona Entrega 3  

### Medición
- Punto Medición 1 – Online - sede Asclepios  
- Punto Medición 2 – Online - sede Asclepios  
- Punto Medición 3 – Online - sede Asclepios  
- Punto Medición 4 – Online - sede Asclepios  
- Punto Medición 5 – Zona Medición 5  
- Punto Medición 6 – Zona Medición 6  
- Punto Medición 7 – Zona Medición 7  
- Punto Medición 8 – Zona Medición 8  
- Punto Medición 9 – Zona Medición 9  
- Punto Medición 10 – Zona Medición 10  
- Punto Medición 11 – Zona Medición 11  

### Recogida
- Punto Recogida 1 – Zona Recogida 1  
- Punto Recogida 2 – Zona Recogida 2  
- Punto Recogida 3 – Zona Recogida 3  
- Punto Recogida 4 – Zona Recogida 4  
- Punto Recogida 5 – Zona Recogida 5  
- Punto Recogida 6 – Zona Recogida 6  
- Punto Recogida 7 – Zona Recogida 7  

---

## 🧩 Plantillas

Dos plantillas base creadas. Una utilizada para crear una misión (crea la misión orgánicamente).

Nota: Aunque todos los transportes, equipo y empleados vengan en la data en estado disponible, al crearse dinámicamente la misión, se activa la automatización y
aquellos en la misión estarán ocupados y el equipo/transporte no disponible.

---

## 📋 Misiones

Una misión creada.


# Grupos, permisos y restricciones de vistas

## Manager (`malkion.group_MANAGER`)

- **Permisos:** Puede ver, crear, editar y eliminar **TODO**.
- **Acceso:** Tiene permisos completos sobre todos los modelos.
- **Vistas:** No tiene restricciones en las vistas ni en los estados.

Nota: Solo los managers tienen acceso a INFORMES.

---

## Agentes de Campo (`malkion.group_AGENTESCAMPO`)

- **Modelos visibles:**
  - `malkion.mission`
  - `malkion.equipo`, `malkion.transport`, `malkion.point_of_interest`, `hr.employee`
  - `malkion.mission_employee_team`, `malkion.mission_employee_transport`

- **Reglas de acceso (`ir.rule`):**
  - Solo pueden ver **misiones en las que están asignados** en `roles_ids`.
  - Solo si el **estado NO es**: `finalizada`, `incidencia_datoprocesando` o `dato_procesando`.

- **Vista específica (`view_malkion_mission_form_agente`):**
  - Solo pueden editar el campo **estado**.
  - El resto de campos está en modo **lectura** (`readonly`).

- **Restricción adicional en el modelo:**
  - Solo pueden cambiar el **estado** a ciertos valores permitidos.
  - **NO** pueden cambiar el estado a `finalizada` ni `incidencia_datoprocesando`.

---

## Asclepios (`malkion.group_ASCLEPIOS`)

- **Modelos visibles:** Igual que *Agentes de Campo* (limitado a misiones y sus relaciones).

- **Reglas de acceso (`ir.rule`):**
  - Solo pueden ver misiones cuyo **estado** sea:
    - `dato_entregado`
    - `incidencia_datoentregado`
    - `dato_procesando`
    - `incidencia_datoprocesando`
    - `finalizada`

- **Vista:** Reutiliza la misma vista que los agentes.
  - Campo **estado** editable, el resto **readonly**.

- **Restricción en el modelo:**
  - Solo pueden cambiar el estado a `finalizada` o `incidencia_datoprocesando`.

---

## Ventas (`malkion.group_VENTAS`)

- **Modelos con permisos completos:** Solo `malkion.contract`
- **Permisos:** Leer, crear, editar y borrar **contratos**.
- **Acceso:** No ve otros modelos.

---

## Logística (`malkion.group_LOGISTICA`)

- **Permisos completos sobre:**
  - `malkion.plantilla` y sus modelos relacionados:
    - `plantilla_equipo`, `plantilla_rol`, `plantilla_transporte`
  - `malkion.almacenes`, `malkion.equipo`, `malkion.transport`, `malkion.point_of_interest`

- **Permisos:** Leer, crear, editar y borrar en los modelos mencionados.

