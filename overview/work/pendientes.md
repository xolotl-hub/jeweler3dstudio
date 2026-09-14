# Pendientes (`overview/work/pendientes.md`)

> Elementos identificados durante la planificación de arquitectura UI para seguimiento en sesiones futuras.

## 📌 Lista de Pendientes

| ID | Fecha detección | Origen / Contexto | Descripción | Estado |
|---|---|---|---|---|
| p1 | 2026-08-27 | Arquitectura UI | Implementación paramétrica del Panel 1: Anillo y Talla (Tallas US 3-13.5, 8 perfiles con Subsurf y Crease). | `hecho` |
| p2 | 2026-08-27 | Arquitectura UI | Visor Modal 3D de Gemas con previsualización, mallas facetadas (6 cortes), materiales BSDF y estimador ct. | `pendiente` |
| p3 | 2026-08-27 | Arquitectura UI | Módulo de Engastes: Garras paramétricas (Prongs), Bisel cerrado (Bezel) y distribución Pavé. | `pendiente` |
| p4 | 2026-08-27 | Arquitectura UI | Módulo de Cortadores Booleanos: Asientos de filetín, perforaciones de luz y cortes en V. | `pendiente` |
| p5 | 2026-08-27 | Arquitectura UI | Módulo de Canastas y Galerías: Generador de biseles inferiores y soportes para piedras centrales. | `pendiente` |
| p6 | 2026-08-27 | Visión Administrativa | Cotizador Administrativo ($/g metal + gemas + mano de obra) y Generador de Ficha Técnica (HTML/PDF). | `pendiente` |
| p7 | 2026-08-27 | Visión Administrativa | Verificador de Seguridad para Impresión 3D/Fundición (Grosor mínimo < 0.8mm y compensación de merma %). | `pendiente` |
| p9 | 2026-09-08 | Iconos de Gemas — Estilos | **Selector de estilo visual de iconos:** Botón o EnumProperty (marquise / round / asscher) para elegir qué set de iconos de gemas se muestra en el panel. Ubicación en UI por definir. Al elegir, el addon copia el estilo activo desde `assets/gems/styles/{estilo}/` hacia `assets/gems/png/` o usa una ruta dinámica. Requiere que los 3 estilos estén completos. | `pendiente` |
| p10 | 2026-09-14 | Gemas — Calibres elongados | Cortes Oval, Pear y Marquise son `L x W` (ej. 6x4mm), pero la UI y el operador solo manejan un eje. Requiere segundo campo de dimensión o tabla fija LxW por preset para calcular volumen/ct correcto. | `pendiente` |
| p11 | 2026-09-14 | Gemas — Preset UI | Al cambiar corte (`j3d_gem_cut`), el `j3d_gem_size_preset` puede quedar con key inválido del corte anterior. Blender no reseta automáticamente EnumProperty dinámicos. Fix: update handler o reset en panel draw. | `pendiente` |
| p12 | 2026-09-14 | Anillos — Aros Cónicos / Graduados | Modulación de ancho/grosor variable a lo largo del recorrido radial (tapered shank / solitario). | `pendiente` |
| p13 | 2026-09-14 | Anillos — Orientación de Creación | Selector de orientación de plano base (Superior XY / Frontal XZ / Lateral YZ) en UI de Talla y Perfil. | `hecho` |

- **Estados:** `pendiente`, `en progreso`, `promovido_a_task`, `descartado`, `hecho`.

---

## ✅ Completados (Historial)

| ID | Fecha Resolución | Origen / Contexto | Descripción / Solución | Agente |
|---|---|---|---|---|
| p8 | 2026-09-01 | Bug Escala - Herramienta Talla | Corregida escala mm→BU en `core/ring.py` dividiendo por `unit_scale` (1 BU = 1 mm). Talla US 7 genera 17.32 BU. | Gemini 3.6 Flash (Medium) |

