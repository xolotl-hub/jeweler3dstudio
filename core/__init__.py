"""
Jeweler 3D Studio - Core Package Initialization
Registers core property groups, geometry operators, and calculation modules.
"""

from . import units
from . import ring
from . import gems

# Módulos secundarios desconectados por el momento
# from . import prongs
# from . import cutters
# from . import pave
# from . import metrics

modules = (
    units,
    ring,
    gems,
)


def register():
    for mod in modules:
        if hasattr(mod, "register"):
            mod.register()


def unregister():
    for mod in reversed(modules):
        if hasattr(mod, "unregister"):
            mod.unregister()
