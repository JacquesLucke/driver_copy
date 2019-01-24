import bpy
from . props import DataPath

class CopyDriverOperator(bpy.types.Operator):
    bl_idname = "object.copy_driver"
    bl_label = "Copy Driver"

    def execute(self, context):
        source_object = context.active_object
        target_objects = set(context.selected_objects) - {source_object}

        settings = context.scene.copy_driver_settings
        for path in settings.iter_paths_to_copy():
            for target_object in target_objects:
                copy_driver_between_objects(
                    source_object, target_object,
                    path, only_available=True)
        return {'FINISHED'}


def copy_driver_between_objects(source, target, path, *, only_available=False):
    src_fcurve = find_driver_fcurve(source, path)
    if src_fcurve is None:
        if only_available:
            return
        else:
            raise Exception("Driver does not exist on source: " + str(path))
    dst_fcurve = new_driver_fcurve(target, path)
    copy_driver(src_fcurve.driver, dst_fcurve.driver)

def copy_driver(src_driver, dst_driver):
    copy_driver_variables(src_driver, dst_driver)
    dst_driver.type = src_driver.type
    dst_driver.expression = src_driver.expression
    dst_driver.use_self = src_driver.use_self

def copy_driver_variables(src_driver, dst_driver):
    for src_variable in src_driver.variables:
        dst_variable = dst_driver.variables.new()
        dst_variable.name = src_variable.name
        dst_variable.type = src_variable.type
        copy_driver_variable_targets(src_variable, dst_variable)

def copy_driver_variable_targets(src_variable, dst_variable):
    for i, src_target in enumerate(src_variable.targets):
        dst_target = dst_variable.targets[i]
        dst_target.bone_target = src_target.bone_target
        dst_target.data_path = src_target.data_path
        dst_target.id = src_target.id
        dst_target.transform_type = src_target.transform_type
        dst_target.transform_space = src_target.transform_space


# API Wrappers
######################################

def find_driver_fcurve(obj, path: DataPath):
    if obj.animation_data is None:
        return None

    if path.use_index:
        return obj.animation_data.drivers.find(path.path, index=path.index)
    else:
        return obj.animation_data.drivers.find(path.path)

def new_driver_fcurve(obj, path: DataPath):
    ensure_animation_data(obj)
    if path.use_index:
        return obj.animation_data.drivers.new(path.path, index=path.index)
    else:
        return obj.animation_data.drivers.new(path.path);

def ensure_animation_data(ob):
    if ob.animation_data is None:
        ob.animation_data_create()