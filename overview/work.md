# Trabajo: índice maestro y backlog canónico

> **Backlog canónico único.** Concentra los IDs de `tarea`, `bug` y `deuda`. El detalle se distribuye en `overview/work/tasks.md` (tarea activa), `overview/work/pendientes.md` (seguimiento) y `overview/work/deuda_tecnica.md` (deuda ordenada por prioridad Alta/Media/Baja).

| ID | Tipo | Estado | Resumen | Archivo de Detalle |
|---|---|---|---|---|

| [flag-p2] | tarea | no verificado | `p2` figura pendiente, pero `w22` registra su implementación y resolución. Consolidar al confirmar en Blender. | `overview/work/pendientes.md` |
| [flag-w22] | bug | no verificado | Historial declara eliminada `target_set_prop("matrix", ...)`, pero aún existe en `ui/gizmos.py:33`. Verificar en Blender y corregir el historial o el código. | `ui/gizmos.py` |


Tipos: `tarea`, `bug`, `deuda`. Estados: `pendiente`, `en progreso`, `bloqueado`, `hecho`, `no verificado`.

---

## ✅ Completados (Historial)

<!-- Mover aquí tareas, bugs o deudas completadas conservando su ID -->

| ID | Tipo | Resuelto por (Agente) | Causa Raíz / Resumen Solución | Fecha |
|---|---|---|---|---|
| w30 | tarea | Gemini 3.7 Flash (Medium) | Selector de orientación de plano (Superior XY, Frontal XZ, Lateral YZ) en Talla (Curva/Cilindro) y Perfil del Metal (Aro 3D). Resuelto `p13`. ZIP empaquetado. | 2026-09-14 |
| w29 | mejora | Gemini 3.7 Flash (Medium) | Modificador Subsurf automático + Edge Crease (`crease_edge` = 0.8) en esquinas vivas del perfil. Selectores de segmentos radiales y resolución de perfil en UI. ZIP empaquetado. | 2026-09-14 |
| w28 | tarea | Gemini 3.7 Flash (Medium) | 8 perfiles paramétricos de metal (Media Caña, Plano, Confort, Oval, Filo, Aro Europeo, Biseado, Cóncavo) con sweep BMesh y diámetro interior = Talla US real. Selector UI y ZIP empaquetado. | 2026-09-14 |
| w27 | tarea | Claude Sonnet 4.6 (Thinking) | 17 cortes x tabla completa de calibres comerciales GIA/ISO con ct estimados por densidad+factor volumétrico. Default=1.0mm (ROUND). ZIP reempaquetado. | 2026-09-14 |
| w26 | tarea | Gemini 3.7 Flash (Medium) | Desplegable de calibres y quilates comerciales estándar (19 calibres 1.0mm-10.0mm GIA) con fallback condicional a `CUSTOM`. | 2026-09-14 |
| w25 | tarea | Gemini 3.7 Flash (Medium) | Normalizadas conversiones mm/BU (`mm_to_bu`), creado `core/units.py`, simplificada UI fijando estándar `1 BU = 1 mm`. | 2026-09-14 |
| w24 | tarea | OpenAI GPT-5 | Generado Round Brilliant Art Déco desde proporciones de tabla, estrella y filetín de `core/gems.py`; SVG y PNG activados. | 2026-09-08 |
| w23 | tarea | Gemini 3.7 Flash (Medium) | Generados 17 iconos vectoriales de lujo (SVG + PNG 256x256 dark/light), backup en `assets_historial/`, y conectado `template_icon_view` con `bpy.utils.previews`. | 2026-09-08 |
| w22 | bug | Gemini 3.7 Flash (Medium) | Eliminada llamada a propiedad inexistente `target_set_prop("matrix", ...)` en `ui/gizmos.py` y asignado `matrix_basis` en `refresh()`. | 2026-09-08 |
| w21 | tarea | Claude Sonnet 4.6 (Thinking) | Reemplazado `j3d.dummy_cube` por `j3d.add_gem` en `ui/panels.py` (Visor de Gemas). Botón ahora genera Diamante 3D facetado de 5mm. | 2026-09-01 |
| w20 | tarea | Gemini 3.6 Flash (Medium) | Ajustado `J3D_OT_dummy_cube` (`core/gems.py`) a tamaño de 5 mm en la escala de joyería (1 BU = 1 mm). | 2026-09-01 |
| w19 | bug | Gemini 3.6 Flash (Medium) | Restaurado `J3D_OT_dummy_cube` en `core/gems.py` devolviendo los botones a los subpaneles UI. | 2026-09-01 |
| w18 | tarea | Gemini 3.6 Flash (Medium) | Operador `J3D_OT_add_gem` (`j3d.add_gem`) en `core/gems.py`: Diamante Redondo 5mm (0.52ct) por defecto, 7 cortes, materiales BSDF e integración en Visor de Gemas (`ui/panels.py`). | 2026-09-01 |
| w17 | bug | Gemini 3.6 Flash (Medium) | Cambiado `spline.points.add(3)` por `spline.bezier_points.add(3)` en `core/ring.py`. Resuelto RuntimeError. | 2026-09-01 |
| w16 | bug | Gemini 3.6 Flash (Medium) | Refactor en `core/ring.py` con `object_data_add(context, obdata, operator=self)` y generadores nativos BMesh/Curve. Corregida alineación View. | 2026-09-01 |
| w15 | bug | Gemini 3.6 Flash (Medium) | Eliminada división por 1000 en `core/ring.py` e implementada escala 1 BU = 1 mm adaptable a `unit_scale`. Talla US 7 mide 17.32 BU. Resuelto `p8`. | 2026-09-01 |
| w14 | tarea | Gemini 3.6 Flash (Medium) | Script `pack_extension.py` en raíz que empaqueta únicamente la extensión de Blender en `dist/jeweler3dstudio-0.1.0.zip` (50 archivos, 444 KB), omitiendo entornos de dev. | 2026-09-01 |
| w13 | tarea | Gemini 3.6 Flash (Medium) | Integración de `AddObjectHelper` en `J3D_OT_create_ring_size` (`core/ring.py`) agregando `align`, `location` y `rotation` al Redo Panel en curvas y cilindros. | 2026-09-01 |
| w1 | tarea | Gemini 3.6 Flash (Medium) | Auditoría completa de extensión Blender 4.2+ (Manifiesto, UI context safety, registro modular). Corregido `core/__init__.py`. | 2026-08-26 |
| w2 | tarea | Gemini 3.6 Flash (Medium) | Generador paramétrico procedural de mallas 3D para gemas en `core/gems.py` con facetas reales (6 cortes), materiales BSDF y estimador de quilates. | 2026-08-27 |
| w3 | tarea | Gemini 3.6 Flash (Medium) | Visor modal interactivo de gemas, presets de tamaño rápido (1.0 a 6.5mm) y operador de edición `j3d.edit_gem`. | 2026-08-27 |
| w4 | tarea | Gemini 3.6 Flash (Medium) | Refactorización de UI a sub-paneles nativos de Blender (`bl_parent_id`), resolviendo el anidamiento visual de cajas. | 2026-08-27 |
| w5 | tarea | Gemini 3.6 Flash (Medium) | Visor modal emergente con `template_icon_view`, iconos PNG de cortes, recuadro de previsualización grande y botones OK/Cancel. | 2026-08-27 |
| w6 | tarea | Gemini 3.6 Flash (Medium) | Estructura de paneles independientes de nivel superior en la pestaña Jeweler 3D (idéntico a Jewelcraft). | 2026-08-27 |
| w7 | tarea | Gemini 3.6 Flash (Medium) | Simplificación de UI a 1 botón funcional ultra-simple por sección (Anillo, Gema, Cortador, Métricas). | 2026-08-27 |
| w8 | tarea | Gemini 3.6 Flash (Medium) | Eliminación del panel `VIEW3D_PT_j3d_gems` ("Gemas y Engastes") de `ui/panels.py`. | 2026-08-27 |
| w9 | tarea | Gemini 3.6 Flash (Medium) | Estructura limpia de 6 paneles y subpaneles con operador base `j3d.dummy_cube` para construcción progresiva. | 2026-08-27 |
| w10 | tarea | Gemini 3.6 Flash (Medium) | Arquitectura completa de 6 paneles y 13 sub-paneles en `ui/panels.py` + Registro del backlog `p1`-`p7` en `pendientes.md`. | 2026-08-27 |
| w11 | tarea | Gemini 3.6 Flash (Medium) | Configuración de `bl_options = {'DEFAULT_CLOSED'}` en sub-paneles excepto Visor de Gemas. | 2026-08-27 |
| w12 | tarea | Gemini 3.6 Flash (Medium) | Herramienta Talla implementada en `core/ring.py` (Tallas US 3.0-13.5 con medias tallas, default US 7.0, selector doble Curva/Cilindro y panel emergente de ajuste). | 2026-08-27 |

---

## 📋 Historial de Intentos

### [w27] Calibres y Quilates Comerciales Dinámicos por Corte

| Fecha | Agente | Intento | Resultado |
|---|---|---|---|
| 2026-09-14 | Gemini 3.7 Flash (Medium) | Implementación de calibres específicos para los 17 cortes x piedra, default a 1.0mm y factores volumétricos | en progreso |
