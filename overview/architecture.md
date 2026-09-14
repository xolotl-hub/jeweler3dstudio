# 🏗️ Arquitectura del Proyecto — Jeweler 3D Studio (Blender 4.2+ Extension)

> **Diagrama vivo de arquitectura y mapa de componentes del Addon de Joyería 3D para Blender 4.2+ / 5.x+**.

---

## 📊 Diagrama de Componentes y Flujo de Ejecución

```mermaid
graph TD
    subgraph Manifest ["📦 Extension Manifest System"]
        M[blender_manifest.toml]
    end

    subgraph EntryPoint ["🚀 Central Lifecycle Management"]
        Init["__init__.py\n(Dynamic Reloading & Submodule Dispatcher)"]
    end

    subgraph UI ["🖥️ UI & Interaction Layer (ui/)"]
        P["panels.py\nVIEW3D_PT_jeweler_3d_studio / PROPERTIES_PT_jeweler_3d_studio\n(N-Panel & Properties Scene Tab Collapsible Sections)"]
        D["dialogs.py\nJ3D_OT_export_report\n(Modal Production Report Exporter)"]
        G["gizmos.py\nJ3D_GGT_gem_controls\n(Interactive 3D Viewport Handles)"]
    end

    subgraph Core ["⚙️ CAD Domain Engine (core/)"]
        Units["units.py\nJ3D_OT_set_scene_units\n(Unit Conversions & Scene Scale Sync)"]
        Ring["ring.py\nJ3D_OT_create_ring_shank\n(US/EU Parametric Shank Curve Generator)"]
        Gems["gems.py\nJ3D_OT_add_gem\n(Gem Cuts & Carat Estimator)"]
        Prongs["prongs.py\nJ3D_OT_add_prongs\n(Parametric Prong Engine)"]
        Pave["pave.py\nJ3D_OT_create_pave\n(Curve/Surface Gem Distribution)"]
        Cutters["cutters.py\nJ3D_OT_add_cutters\n(Boolean Seat & Hole Cutters)"]
        Metrics["metrics.py\n(BMesh Volume & Metal Weight Density Calculations)"]
    end

    subgraph Assets ["🎨 Asset Library (assets/)"]
        NodeGroups["assets/node_groups/\n(Geometry Nodes Templates)"]
    end

    subgraph BlenderAPI ["🔷 Blender 4.2+ Core Runtime (bpy)"]
        BPY_Data[bpy.data / Curves & Meshes]
        BPY_BMesh[bmesh / Evaluated Mesh Volume]
        BPY_Scene[bpy.types.Scene Properties / Units]
    end

    M --> Init
    Init --> UI
    Init --> Core
    Init --> Assets

    P -->|Dispara Operadores| Core
    P -->|Configura Unidades| Units
    D -->|Lee Métricas de Pesaje| Metrics
    G -->|Tiradores en Viewport| BPY_Data

    Units --> BPY_Scene
    Ring --> BPY_Data
    Gems --> BPY_Data
    Prongs --> BPY_Data
    Pave --> BPY_Data
    Cutters --> BPY_Data
    Metrics --> BPY_BMesh
    P --> BPY_Scene
```

---

## 🏛️ Desglose de Capas y Responsabilidades

| Capa | Archivos / Módulos | Clase / Función Principal | Responsabilidad |
|---|---|---|---|
| **Manifiesto** | `blender_manifest.toml` | Standard TOML Manifest | Metadatos de la extensión, versión mínima de Blender (4.2.0), tags y licencias. |
| **Lifecycle** | `__init__.py` | `register()`, `unregister()` | Recarga dinámica `importlib.reload()` y registro simétrico secuencial de paquetes `core`, `ui` y `assets`. |
| **Core Init** | `core/__init__.py` | `register()`, `unregister()` | Punto de montaje modular del motor CAD con verificación resiliente `hasattr`. |
| **UI Init** | `ui/__init__.py` | `register()`, `unregister()` | Registro de paneles N-Panel, diálogos modales y GizmoGroups. |
| **UI Panels** | `ui/panels.py` | `VIEW3D_PT_jeweler_3d_studio` | Interfaz N-Panel responsiva con secciones colapsables (Anillo Base, Gemas, Cortadores, Métricas, Unidades). |
| **UI Dialogs** | `ui/dialogs.py` | `J3D_OT_export_report` | Exportador de fichas técnicas de producción en formato de texto/JSON con peso estimado y volumen. |
| **UI Gizmos** | `ui/gizmos.py` | `J3D_GGT_gem_controls` | Tiradores visuales 3D interactivos en el Viewport para manipulación directa de gemas y cortadores. |
| **Domain: Units** | `core/units.py` | `mm_to_bu()`, `J3D_OT_set_scene_units` | Conversión universal mm/BU y operador para sincronizar Scene Properties a milímetros (0.001 scale / mm). |
| **Domain: Ring** | `core/ring.py` | `J3D_OT_create_ring_size`, `J3D_OT_create_ring_profile` | Generador paramétrico de curvas/mallas de talla US (3.0-13.5), 8 perfiles de metal con sweep BMesh, orientación (Top/Front/Side), Subsurf y Edge Crease (0.8). |
| **Domain: Gems** | `core/gems.py` | `J3D_OT_add_gem` | Creación de piedras preciosas parametrizadas (Redonda, Princesa, Oval, Esmeralda, Pera, Marquesa) y cálculo de quilates. |
| **Domain: Prongs** | `core/prongs.py` | `J3D_OT_add_prongs` | Engaste de garras paramétricas (Redonda, Garra, V-Prong, Cuadrada) vinculadas a la gema activa. |
| **Domain: Pavé** | `core/pave.py` | `J3D_OT_create_pave` | Algoritmo de distribución de gemas sobre curvas 3D y mallas de superficie. |
| **Domain: Cutters** | `core/cutters.py` | `J3D_OT_add_cutters` | Cortadores booleanos para asientos de filetín, perforaciones de entrada de luz y biseles completos. |
| **Domain: Metrics**| `core/metrics.py` | `calculate_mesh_volume_cm3()` | Cálculo preciso de volumen $cm^3$ mediante `bmesh` y peso estimado en Oro (24K, 18K, 14K), Platino, Plata y Titanio. |
| **Assets** | `assets/node_groups/` | Geometry Nodes Library | Plantillas de nodos no destructivos para modificadores de Blender. |
