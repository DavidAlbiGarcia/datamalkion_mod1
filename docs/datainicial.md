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


