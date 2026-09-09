"""
Jeweler 3D Studio - Core Ring Shank & Size Module
Provides parametric generation of ring size references (US Sizes with half sizes)
and ring shank geometry (Bezier Curves / Mesh Cylinders).
"""

from typing import Dict, Tuple, List
import math
import bpy
import bmesh
from bpy.props import EnumProperty, FloatProperty, StringProperty
from bpy.types import Operator, PropertyGroup
from bpy_extras.object_utils import AddObjectHelper, object_data_add

# Complete US Ring Size Chart (US Size -> Inner Diameter in mm)


US_RING_SIZES: Dict[str, float] = {
    "3.0": 14.05,
    "3.5": 14.45,
    "4.0": 14.86,
    "4.5": 15.27,
    "5.0": 15.70,
    "5.5": 16.10,
    "6.0": 16.51,
    "6.5": 16.92,
    "7.0": 17.32,  # Default
    "7.5": 17.73,
    "8.0": 18.14,
    "8.5": 18.54,
    "9.0": 18.95,
    "9.5": 19.35,
    "10.0": 19.76,
    "10.5": 20.17,
    "11.0": 20.57,
    "11.5": 20.98,
    "12.0": 21.39,
    "12.5": 21.79,
    "13.0": 22.20,
    "13.5": 22.61,
}

US_SIZE_ITEMS: List[Tuple[str, str, str]] = [
    (k, f"US {k} ({v:.2f} mm)", f"Talla US {k} - Diámetro interno {v:.2f} mm")
    for k, v in US_RING_SIZES.items()
]

GEOMETRY_TYPE_ITEMS: List[Tuple[str, str, str, str, int]] = [
    ("CURVE", "Curva Bézier", "Genera una curva circular Bézier 3D para el perfil del anillo", "CURVE_NCIRCLE", 0),
    ("CYLINDER", "Cilindro Malla", "Genera una malla 3D de cilindro como referencia de talla", "MESH_CYLINDER", 1),
]

PROFILE_ITEMS: List[Tuple[str, str, str]] = [
    ("MEDIA_CANA", "Media Caña", "Perfil abombado superior y plano inferior"),
    ("PLANO", "Plano", "Perfil rectangular plano tradicional"),
    ("CONFORT", "Confort", "Perfil abombado suave interior y exterior"),
]


def create_ring_bezier_curve(name: str, radius: float) -> bpy.types.Curve:
    """Crea una curva Bézier circular 3D paramétrica con radio dado."""
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('BEZIER')
    spline.use_cyclic_u = True

    # Constante Bézier para una circunferencia perfecta con 4 puntos
    k = 0.5522847498307936 * radius
    points = [
        # (px, py, pz, hrx, hry, hrz, hlx, hly, hlz)
        (radius, 0.0, 0.0,  radius,  k,       0.0,  radius, -k,       0.0),
        (0.0,    radius, 0.0, -k,       radius,  0.0,  k,       radius,  0.0),
        (-radius, 0.0, 0.0, -radius, -k,       0.0, -radius,  k,       0.0),
        (0.0,   -radius, 0.0,  k,      -radius,  0.0, -k,      -radius,  0.0),
    ]
    spline.bezier_points.add(3)

    for i, (px, py, pz, hrx, hry, hrz, hlx, hly, hlz) in enumerate(points):
        bp = spline.bezier_points[i]
        bp.co = (px, py, pz)
        bp.handle_right = (hrx, hry, hrz)
        bp.handle_left = (hlx, hly, hlz)

    return curve_data


def create_ring_cylinder_mesh(name: str, radius: float, depth: float) -> bpy.types.Mesh:
    """Crea una malla 3D de cilindro de referencia paramétrico con BMesh."""
    mesh_data = bpy.data.meshes.new(name=name)
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=64,
        radius1=radius,
        radius2=radius,
        depth=depth
    )
    bm.to_mesh(mesh_data)
    bm.free()
    return mesh_data


class J3D_OT_create_ring_size(Operator, AddObjectHelper):
    """Genera la geometría base de Talla de Anillo (Curva o Cilindro)"""
    bl_idname = "j3d.create_ring_size"
    bl_label = "Crear Talla de Anillo"
    bl_description = "Crea la referencia de talla de anillo según la talla US seleccionada"
    bl_options = {'REGISTER', 'UNDO'}

    us_size: EnumProperty(
        name="Talla US",
        description="Selección de talla estándar US (incluye medias tallas)",
        items=US_SIZE_ITEMS,
        default="7.0"
    ) # type: ignore

    geometry_type: EnumProperty(
        name="Tipo de Geometría",
        description="Formato del objeto de salida (Curva Bézier o Cilindro 3D)",
        items=GEOMETRY_TYPE_ITEMS,
        default="CURVE"
    ) # type: ignore

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return context.mode == 'OBJECT'

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, "us_size", text="Talla US")

        row = layout.row(align=True)
        row.label(text="Tipo de Salida")
        row.prop(self, "geometry_type", expand=True)

        layout.separator()

        layout.prop(self, "align", text="Alineación")
        layout.prop(self, "location", text="Ubicación")
        layout.prop(self, "rotation", text="Rotación")

    def execute(self, context: bpy.types.Context) -> set[str]:
        inner_dia_mm = US_RING_SIZES.get(self.us_size, 17.32)
        # Adaptación a la escala de unidades de la escena (1 BU = 1 mm en joyería)
        unit_scale = context.scene.unit_settings.scale_length
        if unit_scale <= 0:
            unit_scale = 1.0

        # Radio en unidades de escena (milímetros en entorno de joyería)
        radius = (inner_dia_mm / 2.0) / unit_scale
        cylinder_depth = 3.0 / unit_scale  # 3mm de referencia de grosor

        obj_name = f"RingSize_US_{self.us_size}"

        if self.geometry_type == 'CURVE':
            curve_data = create_ring_bezier_curve(obj_name, radius)
            obj = object_data_add(context, curve_data, operator=self)
        else:  # CYLINDER
            mesh_data = create_ring_cylinder_mesh(obj_name, radius, cylinder_depth)
            obj = object_data_add(context, mesh_data, operator=self)

        obj.name = obj_name
        obj["j3d_type"] = "RING_SIZE"
        obj["j3d_us_size"] = self.us_size
        obj["j3d_inner_dia_mm"] = inner_dia_mm

        self.report({'INFO'}, f"Talla US {self.us_size} ({inner_dia_mm:.2f} mm) creada.")
        return {'FINISHED'}





classes = (
    J3D_OT_create_ring_size,
)


def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            try:
                bpy.utils.unregister_class(cls)
                bpy.utils.register_class(cls)
            except Exception:
                pass


def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
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
