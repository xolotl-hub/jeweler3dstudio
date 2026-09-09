# Deuda Técnica (`overview/work/deuda_tecnica.md`)

> Errores, refactors pendientes o problemas no resueltos a nivel de código, ordenados por prioridad de impacto.

## 🔴 Prioridad Alta (Impacto Crítico / Bloqueante)

| ID | Ubicación / Componente | Descripción de la Deuda | Impacto |
|---|---|---|---|
| — | — | Sin deuda crítica activa. | — |

## 🟡 Prioridad Media (Impacto Moderado / Mantenibilidad)

| ID | Ubicación / Componente | Descripción de la Deuda | Impacto |
|---|---|---|---|
| d2 | `ui/panels.py` (328L) | Archivo supera 250L — candidato a refactor por subpaneles en archivos separados. | Mantenibilidad. |
| d5 | `core/gems.py` (285L) | Módulo supera 250L — separar motor geométrico de operadores/previews. | Mantenibilidad. |

## 🟢 Prioridad Baja (Mejora Menor / Estilo)

| ID | Ubicación / Componente | Descripción de la Deuda | Impacto |
|---|---|---|---|
| d4 | `overview/work.md` | Filas de historial con líneas vacías entre entradas — inconsistencia de formato. | Visual / menor. |
| d6 | `tools/generate_gem_icons.py` (459L) | Script de generación supera 250L — modularizar por estilo/corte. | Dev tooling. |

---

## ✅ Completados (Historial)

| ID | Ubicación / Componente | Descripción de la Deuda | Solución Aplicada | Agente | Fecha |
|---|---|---|---|---|---|
| d1 | `core/gems.py` / `J3D_OT_add_gem` | Geometría del diamante incompleta: solo pabellón (cono primitivo). | `create_round_brilliant_mesh()` procedural 57 facetas (corona + filetín + pabellón). | Gemini 3.7 Flash (Medium) | 2026-09-08 |
| d3 | `core/gems.py` | Funciones `create_gem_mesh`, `GEM_TYPES`, `CUT_ITEMS`, `GEM_TYPE_ITEMS` no usadas. | Eliminadas en refactor; reemplazadas por `CUT_DEFS` + `create_round_brilliant_mesh`. | Composer | 2026-09-08 |
| - | `ui/panels.py` | `icon='GEM'` no existe en Blender 5.2 — causaba crash silencioso en draw() ocultando botón. | Cambiado a `icon='MESH_ICOSPHERE'`. | Claude Sonnet 4.6 (Thinking) | 2026-09-01 |
| - | `core/ring.py` | `spline.points.add()` en spline BEZIER lanzaba RuntimeError. | Cambiado a `spline.bezier_points.add()`. | Gemini 3.6 Flash (Medium) | 2026-09-01 |
