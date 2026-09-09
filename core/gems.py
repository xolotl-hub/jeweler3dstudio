"""
Jeweler 3D Studio - Core Gems Module
Provides 3D gem generation, preview icon integration (17 luxury cuts),
realistic BSDF material generation, carat estimation, and UI operators.
"""

import os
import math
import bpy
import bmesh
import bpy.utils.previews
from bpy.props import EnumProperty, FloatProperty
from bpy.types import Operator

# ── 17 Gem Cut Definitions & Icon Mappings ───────────────────────────────────
CUT_DEFS = [
    ("ROUND",     "Redondo",   "round.png"),
    ("OVAL",      "Oval",      "oval.png"),
    ("CUSHION",   "Cushion",   "cushion.png"),
    ("PEAR",      "Pera",      "pear.png"),
    ("MARQUISE",  "Marquesa",  "marquise.png"),
    ("PRINCESS",  "Princesa",  "princess.png"),
    ("BAGUETTE",  "Baguette",  "baguette.png"),
    ("SQUARE",    "Cuadrado",  "square.png"),
    ("EMERALD",   "Esmeralda", "emerald.png"),
    ("ASSCHER",   "Asscher",   "asscher.png"),
    ("RADIANT",   "Radiante",  "radiant.png"),
    ("FLANDERS",  "Flanders",  "flanders.png"),
    ("OCTAGON",   "Octagono",  "octagon.png"),
    ("HEART",     "Corazon",   "heart.png"),
    ("TRILLION",  "Trillon",   "trillion.png"),
    ("TRILLIANT", "Trillante", "trilliant.png"),
    ("TRIANGLE",  "Triangulo", "triangle.png"),
]

# ── Gem Stones & Physical Properties ─────────────────────────────────────────
GEM_STONES = {
    "DIAMOND":       {"name": "Diamante",   "ior": 2.417, "density": 3.52, "color": (1.0, 1.0, 1.0, 1.0)},
    "RUBY":          {"name": "Rubi",       "ior": 1.770, "density": 4.02, "color": (0.85, 0.02, 0.08, 1.0)},
    "SAPPHIRE":      {"name": "Zafiro",     "ior": 1.770, "density": 4.02, "color": (0.05, 0.15, 0.85, 1.0)},
    "EMERALD":       {"name": "Esmeralda",  "ior": 1.580, "density": 2.76, "color": (0.02, 0.75, 0.25, 1.0)},
    "AQUAMARINE":    {"name": "Aquamarina", "ior": 1.575, "density": 2.72, "color": (0.35, 0.85, 0.95, 1.0)},
    "AMETHYST":      {"name": "Amatista",   "ior": 1.544, "density": 2.65, "color": (0.45, 0.08, 0.65, 1.0)},
    "CUBIC_ZIRCONIA":{"name": "Circonia",   "ior": 2.150, "density": 5.65, "color": (0.95, 0.95, 1.0, 1.0)},
    "MOISSANITE":    {"name": "Moissanita", "ior": 2.650, "density": 3.22, "color": (0.98, 0.99, 1.0, 1.0)},
    "MORGANITE":     {"name": "Morganita",  "ior": 1.580, "density": 2.76, "color": (0.95, 0.65, 0.60, 1.0)},
    "TANZANITE":     {"name": "Tanzanita",  "ior": 1.695, "density": 3.35, "color": (0.20, 0.15, 0.75, 1.0)},
}

STONE_ITEMS = [(k, v["name"], f"Piedra {v['name']}") for k, v in GEM_STONES.items()]

# ── Preview Collections Management ───────────────────────────────────────────
_preview_collections = {}


def get_cut_preview_collection():
    """Carga y cachea los iconos PNG de los 17 cortes.
    Busca primero en assets/gems/png (generados por el script),
    con fallback a assets/gems/dark (iconos legacy).
    """
    global _preview_collections
    if "cuts" in _preview_collections:
        return _preview_collections["cuts"]

    pcoll = bpy.utils.previews.new()
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Prioridad: png/ (script) → dark/ (legacy)
    png_dir  = os.path.join(base_dir, "assets", "gems", "png")
    dark_dir = os.path.join(base_dir, "assets", "gems", "dark")
    icons_dir = png_dir if os.path.isdir(png_dir) else dark_dir

    if os.path.isdir(icons_dir):
        for key, label, icon_file in CUT_DEFS:
            if key != "ROUND":
                continue
            icon_path = os.path.join(icons_dir, icon_file)
            if not os.path.isfile(icon_path):
                icon_path = os.path.join(icons_dir, f"{key.lower()}.png")
            if os.path.isfile(icon_path):
                pcoll.load(key, icon_path, 'IMAGE')

    _preview_collections["cuts"] = pcoll
    return pcoll


def clear_previews():
    """Libera la memoria de previews al desregistrar."""
    global _preview_collections
    for pcoll in _preview_collections.values():
        try:
            bpy.utils.previews.remove(pcoll)
        except Exception:
            pass
    _preview_collections.clear()


def get_cut_enum_items(self, context):
    """Callback dinámico para EnumProperty con iconos de previsualización."""
    try:
        pcoll = get_cut_preview_collection()
    except Exception:
        pcoll = None

    items = []
    for i, (key, label, icon_file) in enumerate(CUT_DEFS):
        icon_id = 0
        if key == "ROUND" and pcoll is not None and key in pcoll:
            icon_id = pcoll[key].icon_id
        items.append((key, label, f"Corte {label}", icon_id, i))
    return items


# ── Carat Weight Estimator ───────────────────────────────────────────────────
def calculate_carats(stone_key: str, cut_key: str, size_mm: float) -> float:
    """Calcula el peso estimado en quilates basado en densidad física y volumen."""
    density = GEM_STONES.get(stone_key, GEM_STONES["DIAMOND"])["density"]
    # Calibración: Diamante Redondo 5.0mm = ~0.52 ct
    base_ct = (size_mm / 5.0) ** 3 * 0.52 * (density / 3.52)
    return round(base_ct, 3)


# ── BSDF Material Builder ────────────────────────────────────────────────────
def get_or_create_gem_material(stone_key: str):
    """Crea o reutiliza un material BSDF realista para la gema seleccionada."""
    mat_name = "J3D_Material_" + stone_key
    mat = bpy.data.materials.get(mat_name)
    if mat is not None:
        return mat

    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    props = GEM_STONES.get(stone_key, GEM_STONES["DIAMOND"])
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value = 1.0

    bsdf.inputs['Base Color'].default_value = props["color"]
    bsdf.inputs['Roughness'].default_value = 0.0
    bsdf.inputs['IOR'].default_value = props["ior"]
    return mat


# ── Procedural Gem Geometry Engine ───────────────────────────────────────────
def create_round_brilliant_mesh(name: str = "Round_Diamond_Mesh", size_mm: float = 5.0, unit_scale: float = 1.0) -> bpy.types.Mesh:
    """Genera una malla 3D procedural paramétrica de Talla Brillante Redonda (57 facetas).
    
    unit_scale: context.scene.unit_settings.scale_length
    Blender internal: 1 BU = 1 m / unit_scale
    Conversion: size_mm → meters (/ 1000) → BU (/ unit_scale)
    """
    # Tamaño en Blender Units: mm → m → BU
    diameter = (size_mm / 1000.0) / unit_scale
    radius = diameter / 2.0
    r_table = radius * 0.56
    r_star = radius * 0.77
    r_girdle = radius

    z_table = 0.145 * diameter
    z_star = 0.095 * diameter
    z_upper_girdle = 0.0175 * diameter
    z_lower_girdle = -0.0175 * diameter
    z_culet = -0.430 * diameter

    bm = bmesh.new()

    # 1. Vértices
    v_culet = bm.verts.new((0.0, 0.0, z_culet))

    # Tabla
    v_table = []
    for i in range(8):
        angle = i * (2.0 * math.pi / 8.0) + (math.pi / 8.0)
        v_table.append(bm.verts.new((r_table * math.cos(angle), r_table * math.sin(angle), z_table)))

    # Corona / Estrella
    v_star = []
    for i in range(8):
        angle = i * (2.0 * math.pi / 8.0)
        v_star.append(bm.verts.new((r_star * math.cos(angle), r_star * math.sin(angle), z_star)))

    # Filetín Superior
    v_ug = []
    for k in range(16):
        angle = k * (2.0 * math.pi / 16.0)
        v_ug.append(bm.verts.new((r_girdle * math.cos(angle), r_girdle * math.sin(angle), z_upper_girdle)))

    # Filetín Inferior
    v_lg = []
    for k in range(16):
        angle = k * (2.0 * math.pi / 16.0)
        v_lg.append(bm.verts.new((r_girdle * math.cos(angle), r_girdle * math.sin(angle), z_lower_girdle)))

    bm.verts.ensure_lookup_table()

    # 2. Caras
    bm.faces.new([v_table[7], v_table[6], v_table[5], v_table[4], v_table[3], v_table[2], v_table[1], v_table[0]])

    for i in range(8):
        prev_i = (i - 1) % 8
        bm.faces.new([v_table[prev_i], v_table[i], v_star[i]])

    for i in range(8):
        next_i = (i + 1) % 8
        ug_idx = (2 * i + 1) % 16
        bm.faces.new([v_table[i], v_star[next_i], v_ug[ug_idx], v_star[i]])

    for i in range(8):
        ug_mid = (2 * i + 1) % 16
        ug_center = (2 * i) % 16
        ug_prev = (2 * i - 1) % 16
        bm.faces.new([v_star[i], v_ug[ug_mid], v_ug[ug_center]])
        bm.faces.new([v_star[i], v_ug[ug_center], v_ug[ug_prev]])

    for k in range(16):
        next_k = (k + 1) % 16
        bm.faces.new([v_ug[k], v_ug[next_k], v_lg[next_k], v_lg[k]])

    for k in range(16):
        next_k = (k + 1) % 16
        bm.faces.new([v_culet, v_lg[k], v_lg[next_k]])

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()

    mesh.update()
    return mesh


# ── Operators ─────────────────────────────────────────────────────────────────
class J3D_OT_dummy_cube(Operator):
    """Aniadir Cubo de Prueba 5mm"""
    bl_idname = "j3d.dummy_cube"
    bl_label = "Aniadir Cubo"
    bl_description = "Aniade un cubo de 5mm de referencia a la escena"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        unit_scale = context.scene.unit_settings.scale_length or 1.0
        cube_size = 5.0 / unit_scale
        bpy.ops.mesh.primitive_cube_add(
            size=cube_size,
            location=context.scene.cursor.location
        )
        self.report({'INFO'}, "Cubo de 5 mm creado.")
        return {'FINISHED'}


class J3D_OT_add_gem(Operator):
    """Aniadir Gema 3D Facetada"""
    bl_idname = "j3d.add_gem"
    bl_label = "Aniadir Gema 3D"
    bl_description = "Aniade una gema 3D facetada en la posicion del cursor 3D"
    bl_options = {'REGISTER', 'UNDO'}

    cut: EnumProperty(name="Corte", items=get_cut_enum_items)
    stone: EnumProperty(name="Piedra", items=STONE_ITEMS, default="DIAMOND")
    size: FloatProperty(name="Tamano (mm)", default=5.0, min=0.5, max=50.0, step=10, precision=2)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        # Tomar valores de escena si no se pasaron como argumentos
        scene = context.scene
        cut_key = self.cut if self.cut else getattr(scene, "j3d_gem_cut", "ROUND")
        stone_key = self.stone if self.stone else getattr(scene, "j3d_gem_stone", "DIAMOND")
        size_mm = self.size if self.size > 0.0 else getattr(scene, "j3d_gem_size", 5.0)

        unit_scale = context.scene.unit_settings.scale_length or 1.0
        mesh_data = create_round_brilliant_mesh(
            name=f"Gem_{cut_key.title()}_{size_mm:.1f}mm_Mesh",
            size_mm=size_mm,
            unit_scale=unit_scale
        )

        obj = bpy.data.objects.new(f"Gem_{stone_key.title()}_{cut_key.title()}_{size_mm:.1f}mm", mesh_data)
        context.collection.objects.link(obj)
        obj.location = context.scene.cursor.location

        obj["j3d_type"] = "GEM"
        obj["j3d_gem_cut"] = cut_key
        obj["j3d_gem_stone"] = stone_key
        obj["j3d_gem_size"] = size_mm

        ct = calculate_carats(stone_key, cut_key, size_mm)
        obj["j3d_carat"] = ct

        mat = get_or_create_gem_material(stone_key)
        if not obj.data.materials:
            obj.data.materials.append(mat)
        else:
            obj.data.materials[0] = mat

        for o in context.selected_objects:
            o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj

        self.report({'INFO'}, f"Gema {stone_key} {cut_key} ({size_mm:.1f} mm / {ct:.3f} ct) creada con éxito.")
        return {'FINISHED'}


classes = (
    J3D_OT_dummy_cube,
    J3D_OT_add_gem,
)


def register():
    for cls in classes:
        if hasattr(bpy.types, cls.__name__):
            try:
                bpy.utils.unregister_class(getattr(bpy.types, cls.__name__))
            except Exception:
                pass
        try:
            bpy.utils.register_class(cls)
        except Exception:
            pass


def unregister():
    for cls in reversed(classes):
        if hasattr(bpy.types, cls.__name__):
            try:
                bpy.utils.unregister_class(getattr(bpy.types, cls.__name__))
            except Exception:
                pass
        else:
            try:
                bpy.utils.unregister_class(cls)
            except Exception:
                pass
    clear_previews()
