import bpy

class CopyDriversPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Misc"
    bl_label = "Copy Driver"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        settings = context.scene.copy_driver_settings
        col.prop(settings, "path_set", text="")
        if settings.path_set == "CUSTOM":
            col.prop(settings, "custom_path_type", text="")
            col.prop(settings, "custom_data_path", text="Path", icon="RNA")
            if settings.custom_path_type == "PATH_AND_INDEX":
                col.prop(settings, "custom_array_index", text="Index")

        layout.operator("object.copy_driver")