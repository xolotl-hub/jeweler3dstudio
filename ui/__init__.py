"""
Jeweler 3D Studio - UI Package Initialization
Registers user interface panels, dialogs, and viewport gizmo groups.
"""

from . import panels

# Desconectados por el momento
# from . import dialogs
# from . import gizmos

modules = (
    panels,
)


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()
