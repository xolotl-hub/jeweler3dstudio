# Pendientes (`overview/work/pendientes.md`)

> Elementos identificados durante la planificación de arquitectura UI para seguimiento en sesiones futuras.

## 📌 Lista de Pendientes

| ID | Fecha detección | Origen / Contexto | Descripción | Estado |
|---|---|---|---|---|
| p1 | 2026-08-27 | Arquitectura UI | Implementación paramétrica del Panel 1: Anillo y Talla (Tallas US 4-13, perfiles Media Caña/Plano/Confort). | `pendiente` |
| p2 | 2026-08-27 | Arquitectura UI | Visor Modal 3D de Gemas con previsualización, mallas facetadas (6 cortes), materiales BSDF y estimador ct. | `pendiente` |
| p3 | 2026-08-27 | Arquitectura UI | Módulo de Engastes: Garras paramétricas (Prongs), Bisel cerrado (Bezel) y distribución Pavé. | `pendiente` |
| p4 | 2026-08-27 | Arquitectura UI | Módulo de Cortadores Booleanos: Asientos de filetín, perforaciones de luz y cortes en V. | `pendiente` |
| p5 | 2026-08-27 | Arquitectura UI | Módulo de Canastas y Galerías: Generador de biseles inferiores y soportes para piedras centrales. | `pendiente` |
| p6 | 2026-08-27 | Visión Administrativa | Cotizador Administrativo ($/g metal + gemas + mano de obra) y Generador de Ficha Técnica (HTML/PDF). | `pendiente` |
| p7 | 2026-08-27 | Visión Administrativa | Verificador de Seguridad para Impresión 3D/Fundición (Grosor mínimo < 0.8mm y compensación de merma %). | `pendiente` |
| p9 | 2026-09-08 | Iconos de Gemas — Estilos | **Selector de estilo visual de iconos:** Botón o EnumProperty (marquise / round / asscher) para elegir qué set de iconos de gemas se muestra en el panel. Ubicación en UI por definir. Al elegir, el addon copia el estilo activo desde `assets/gems/styles/{estilo}/` hacia `assets/gems/png/` o usa una ruta dinámica. Requiere que los 3 estilos estén completos. | `pendiente` |

- **Estados:** `pendiente`, `en progreso`, `promovido_a_task`, `descartado`, `hecho`.

---

## ✅ Completados (Historial)

| ID | Fecha Resolución | Origen / Contexto | Descripción / Solución | Agente |
|---|---|---|---|---|
| p8 | 2026-09-01 | Bug Escala - Herramienta Talla | Corregida escala mm→BU en `core/ring.py` dividiendo por `unit_scale` (1 BU = 1 mm). Talla US 7 genera 17.32 BU. | Gemini 3.6 Flash (Medium) |

