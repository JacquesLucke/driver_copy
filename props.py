import bpy
import dataclasses
from bpy.props import *

@dataclasses.dataclass
class DataPath:
    path: str
    index: int = dataclasses.field(default=-1)

    @property
    def use_index(self):
        return self.index >= 0

class CopyDriverSettings(bpy.types.PropertyGroup):
    path_set: EnumProperty(name="Path Set", items=[
        ("LOCATION", "Location", ""),
        ("ROTATION", "Rotation", ""),
        ("SCALE", "Scale", ""),
        ("CUSTOM", "Custom", ""),
    ])

    custom_path_type: EnumProperty(name="Path Type", items=[
        ("PATH", "Path", ""),
        ("PATH_AND_INDEX", "Path and Index", ""),
    ])

    custom_data_path: StringProperty(name="Data Path")
    custom_array_index: IntProperty(name="Array Index")

    def iter_paths_to_copy(self):
        if self.path_set == "LOCATION":
            yield DataPath("location", 0)
            yield DataPath("location", 1)
            yield DataPath("location", 2)
        elif self.path_set == "ROTATION":
            yield DataPath("rotation_euler", 0)
            yield DataPath("rotation_euler", 1)
            yield DataPath("rotation_euler", 2)
        elif self.path_set == "SCALE":
            yield DataPath("scale", 0)
            yield DataPath("scale", 1)
            yield DataPath("scale", 2)
        elif self.path_set == "CUSTOM":
            if self.custom_path_type == "PATH":
                yield DataPath(self.custom_data_path)
            elif self.custom_path_type == "PATH_AND_INDEX":
                yield DataPath(self.custom_data_path, self.custom_array_index)

def register():
    bpy.types.Scene.copy_driver_settings = PointerProperty(type=CopyDriverSettings)

def unregister():
    del bpy.types.Scene.copy_driver_settings
