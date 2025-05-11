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

