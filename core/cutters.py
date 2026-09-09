"""
Jeweler 3D Studio - Core Cutters Module
Minimal fail-proof cutter operator for base UI setup.
"""

import bpy
from bpy.types import Operator


class J3D_OT_add_cutters(Operator):
    """Añadir Cortador Base"""
    bl_idname = "j3d.add_cutters"
    bl_label = "Añadir Cortador"
    bl_description = "Añade un cortador booleano base a la escena"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return context.mode == 'OBJECT'

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.002,
            depth=0.005,
            location=context.scene.cursor.location
        )
        obj = context.active_object
        obj.name = "Cutter_Base"
        obj["j3d_type"] = "CUTTER"
        self.report({'INFO'}, "Cortador base añadido.")
        return {'FINISHED'}


classes = (
    J3D_OT_add_cutters,
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
