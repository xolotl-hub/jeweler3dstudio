# Tarea Activa (`overview/work/tasks.md`)

> Espacio de trabajo activo para la tarea en ejecución. Escribir aquí antes de modificar código.

## 🎯 Tarea Activa (Ninguna en ejecución)

- **Última completada:** `[w24]` — `round.svg` y `round.png` en estilo Marquise Art Déco, activados para el visor.
- **Siguiente candidato:** `oval.png` en estilo Marquise Art Déco.

## 🏷️ Clasificación

- [ ] **Problema (Bug):** Comportamiento inesperado o fallo funcional.
- [X] **Mejora (Feature):** Nueva capacidad o refactor de valor.
- [ ] **Deuda / Refactor:** Limpieza de código o estructuración técnica.

## <ctrl42> Rutas de Trabajo y Posibles Soluciones

### Hipótesis / Diagnóstico inicial
- Reutilizar proporciones de tabla, estrella y filetín de `create_round_brilliant_mesh()`.
- Convertir solo esas aristas visibles a icono Art Déco oro sobre negro.

### Ruta elegida
- Generador vectorial basado en la topología existente; rasterización a PNG 256×256.
