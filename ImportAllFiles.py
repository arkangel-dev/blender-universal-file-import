# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8 compliant>

bl_info = {
    "name": "Import All File Types",
    "author": "Sambo",
    "version": (0, 0, 1),
    "blender": (3, 0, 1),
    "location": "File > Import > Import File",
    "description": "Import files into the scene based on the file format",
    "warning": "",
    "support": 'OFFICIAL',
    "category": "Import-Export",
}

from cProfile import label
from cgitb import text
from email.policy import default
from msilib.schema import Icon
from operator import iconcat
from unicodedata import name
from wsgiref import validate
import bpy
from bpy_extras.io_utils import ImportHelper


def read_some_data(context, filepath, ):
    file_extension = filepath.split('.')[-1]
    bpy.types.Scene.targeted_file = filepath
    if (file_extension.lower() in ['dae']): bpy.ops.wm.uni_import_collada('INVOKE_DEFAULT')
    if (file_extension.lower() in ['abc']): bpy.ops.wm.uni_import_alembic('INVOKE_DEFAULT')
    if (file_extension.lower() in ['usd', 'usda', 'usdc']): bpy.ops.wm.uni_import_usd('INVOKE_DEFAULT')
    if (file_extension.lower() in ['svg']): bpy.ops.wm.uni_import_svggp('INVOKE_DEFAULT')
    return {'FINISHED'}

class WM_OT_ImportCollada(bpy.types.Operator):
    bl_label = "Import Collada File"
    bl_idname = "wm.uni_import_collada"

    def execute(self, context):
        print("Importing " + bpy.types.Scene.targeted_file)
        bpy.ops.wm.collada_import(
            filepath=bpy.types.Scene.targeted_file,
            import_units=context.scene.collada_import_units,
            fix_orientation=context.scene.collada_fix_leaf_bones,
            auto_connect=context.scene.collada_auto_correct,
            min_chain_length=context.scene.collada_minimum_chain_length,
            find_chains=context.scene.collada_find_bone_chains)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        
        import_data_options = layout.box()
        import_data_options.label(text='Import Data Options', icon='MESH_DATA')
        import_data_options.prop(context.scene, 'collada_import_units')

        armature_options = layout.box()
        armature_options.label(text="Armature Options", icon='ARMATURE_DATA')

        col = armature_options.column()
        col.prop(context.scene, 'collada_fix_leaf_bones')
        col.prop(context.scene, 'collada_find_bone_chains')
        col.prop(context.scene, 'collada_auto_correct')
        col.prop(context.scene, 'collada_minimum_chain_length')

        last_box = layout.box()
        last_box.prop(context.scene, 'collada_keep_bind_info')
class WM_OT_ImportAlembic(bpy.types.Operator):
    bl_label = "Import Alembic File"
    bl_idname = "wm.uni_import_alembic"

    def execute(self, context):
        bpy.ops.wm.alembic_import(
            filepath=context.scene.targeted_file,
            relative_path=context.scene.alembic_relative_path,
            set_frame_range=context.scene.alembic_set_frame_range,
            is_sequence=context.scene.alembic_is_sequence,
            validate_meshes=context.scene.alembic_validate_meshes,
            always_add_cache_reader=context.scene.alembic_always_add_cache_reader
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        manual_transform_box = layout.box()
        manual_transform_box.label(text="Manual Transform")
        manual_transform_box.prop(context.scene, 'alembic_scale')

        options_box = layout.box()
        options_box.label(text='Options')
        options_box_col = options_box.column()
        options_box_col.prop(context.scene, 'alembic_relative_path')
        options_box_col.prop(context.scene, 'alembic_set_frame_range')
        options_box_col.prop(context.scene, 'alembic_is_sequence')
        options_box_col.prop(context.scene, 'alembic_validate_meshes')
        options_box_col.prop(context.scene, 'alembic_always_add_cache_reader')   
class WM_OT_ImportUniversalSceneDescription(bpy.types.Operator):
    bl_label = "Import USD File"
    bl_idname = "wm.uni_import_usd"

    def execute(self, context):
        bpy.ops.wm.usd_import(
            filepath=context.scene.targeted_file,
            import_cameras=context.scene.usd_dt_camera,
            import_curves=context.scene.usd_dt_curves,
            import_lights=context.scene.usd_dt_lights,
            import_materials=context.scene.usd_dt_materials,
            import_meshes=context.scene.usd_dt_meshes,
            import_volumes=context.scene.usd_dt_volumes,

            prim_path_mask=context.scene.usd_path_mask,
            scale=context.scene.usd_scale,

            read_mesh_uvs=context.scene.usd_md_uv_coords,
            read_mesh_colors=context.scene.usd_md_vertex_colors,
            
            import_subdiv=context.scene.usd_md_incl_subdivision,
            import_instance_proxies=context.scene.usd_md_incl_import_instance_proxies,
            import_visible_only=context.scene.usd_md_incl_visible_primitives_only,
            import_guide=context.scene.usd_md_incl_guide,
            import_proxy=context.scene.usd_md_incl_proxy,
            import_render=context.scene.usd_md_incl_render,
            
            set_frame_range=context.scene.usd_md_opt_set_frame_range,
            relative_path=context.scene.usd_md_opt_relative_path,
            create_collection=context.scene.usd_md_opt_collection,
            light_intensity_scale=context.scene.usd_md_light_intensity_scale,

            import_usd_preview=context.scene.usd_md_exp_import_usd_preview,
            set_material_blend=context.scene.usd_md_exp_set_material_blend
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        first_box = layout.box()
        first_box_first_row = first_box.row()
        data_types_label_col = first_box_first_row.column()
        data_types_checkbox_col = first_box_first_row.column()

        data_types_label_col.label(text='Data Type')
        data_types_checkbox_col.prop(context.scene, 'usd_dt_camera')
        data_types_checkbox_col.prop(context.scene, 'usd_dt_curves')
        data_types_checkbox_col.prop(context.scene, 'usd_dt_lights')
        data_types_checkbox_col.prop(context.scene, 'usd_dt_materials')
        data_types_checkbox_col.prop(context.scene, 'usd_dt_meshes')
        data_types_checkbox_col.prop(context.scene, 'usd_dt_volumes')

        first_box.prop(context.scene, 'usd_path_mask')
        first_box.prop(context.scene, 'usd_scale')

        second_box = layout.box()
        mesh_data_row = second_box.row()
        mesh_data_label_col = mesh_data_row.column()
        mesh_data_checkbox_col = mesh_data_row.column()

        mesh_data_label_col.label(text='Mesh Data')
        mesh_data_checkbox_col.prop(context.scene, 'usd_md_uv_coords')
        mesh_data_checkbox_col.prop(context.scene, 'usd_md_vertex_colors')
        
        include_row = second_box.row()
        include_label_col = include_row.column()
        include_checkbox_col = include_row.column()

        include_label_col.label(text='Include')
        include_checkbox_col.prop(context.scene, 'usd_md_incl_subdivision')
        include_checkbox_col.prop(context.scene, 'usd_md_incl_import_instance_proxies')
        include_checkbox_col.prop(context.scene, 'usd_md_incl_visible_primitives_only')
        include_checkbox_col.prop(context.scene, 'usd_md_incl_guide')
        include_checkbox_col.prop(context.scene, 'usd_md_incl_proxy')
        include_checkbox_col.prop(context.scene, 'usd_md_incl_render')

        options_row = second_box.row()
        options_row_label_col = options_row.column()
        options_row_checkbox_col = options_row.column()

        options_row_label_col.label(text='Options')
        options_row_checkbox_col.prop(context.scene, 'usd_md_opt_set_frame_range')
        options_row_checkbox_col.prop(context.scene, 'usd_md_opt_relative_path')
        options_row_checkbox_col.prop(context.scene, 'usd_md_opt_collection')

        second_box.prop(context.scene, 'usd_md_light_intensity_scale')

        # Third Box
        third_box = layout.box()
        experimental_row = third_box.row()
        experimental_row_label_col = experimental_row.column()
        experimental_row_checkbox_col = experimental_row.column()
        experimental_row_label_col.label(text='Experimental')
        experimental_row_checkbox_col.prop(context.scene, 'usd_md_exp_import_usd_preview')
        experimental_row_checkbox_col.prop(context.scene, 'usd_md_exp_set_material_blend')
class WM_OT_ImportSVGAsGreasePencil(bpy.types.Operator):
    bl_label = "Import SVG as Grease Pencil"
    bl_idname = "wm.uni_import_svggp"

    def execute(self, context):
        bpy.ops.wm.gpencil_import_svg(
            filepath=context.scene.targeted_file,
            resolution=context.scene.svg_gp_resolution,
            scale=context.scene.svg_gp_scale)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, 'svg_gp_resolution')
        layout.prop(context.scene, 'svg_gp_scale')

class TEST_OT_ImportSomeData(bpy.types.Operator, ImportHelper):
    bl_label = "Import Some Data"
    bl_idname = "import_test.some_data"
    
    def execute(self, context):
        return read_some_data(context, self.filepath, )

def view3d_menu_add(self, context, ):
    self.layout.separator()
    self.layout.operator("import_test.some_data", text='Import File', icon='FILEBROWSER')


def register():
    bpy.utils.register_class(TEST_OT_ImportSomeData)
    bpy.utils.register_class(WM_OT_ImportCollada)
    bpy.utils.register_class(WM_OT_ImportAlembic)
    bpy.utils.register_class(WM_OT_ImportUniversalSceneDescription)
    bpy.utils.register_class(WM_OT_ImportSVGAsGreasePencil)
    
    bpy.types.TOPBAR_MT_file_import.append(view3d_menu_add)
    bpy.types.Scene.targeted_file = ""

    # Collada
    bpy.types.Scene.collada_import_units = bpy.props.BoolProperty(name = 'Import Units', description="If disabled match import to Blender's current Unit settings, otherwise use the settings from the Imported scene", default=False)
    bpy.types.Scene.collada_fix_leaf_bones = bpy.props.BoolProperty(name="Fix Leaf Bones", description="Fix Orientation of Leaf Bones (Collada does only support joints)")
    bpy.types.Scene.collada_find_bone_chains = bpy.props.BoolProperty(name="Find Bone Chains", description="Find best matching Bone Chains and ensure bones in chain are connected")
    bpy.types.Scene.collada_auto_correct = bpy.props.BoolProperty(name="Auto Correct", description="set use_connect for parent bones which have exactly one child bone")
    bpy.types.Scene.collada_minimum_chain_length = bpy.props.IntProperty(name="Minimum Chain Length", description="When searching Bone Chains disregard chains of length below this value")
    bpy.types.Scene.collada_keep_bind_info = bpy.props.BoolProperty(name="Keep Bind Info", description="Sotre Bindpose information in custom bone properties for later use during Collada export")

    # Alembic
    bpy.types.Scene.alembic_scale = bpy.props.FloatProperty(name = 'Scale', description='Value by which to enlarge or shrink the objects with respect to the worlds origin')
    bpy.types.Scene.alembic_relative_path = bpy.props.BoolProperty(name = 'Relative Path', description='Select the relative to the blend file')
    bpy.types.Scene.alembic_set_frame_range = bpy.props.BoolProperty(name='Set Frame Range', description='If checked, update scenes start and end frame to match those of the Alembic archive')
    bpy.types.Scene.alembic_is_sequence = bpy.props.BoolProperty(name='Is Sequence', description='Set to true if the cache is split into separate files')
    bpy.types.Scene.alembic_validate_meshes = bpy.props.BoolProperty(name='Validate Meshes', description='Check imported mesh objects for invalid data (slow)')
    bpy.types.Scene.alembic_always_add_cache_reader = bpy.props.BoolProperty(name='Always Add Cache Reader', description='Add cache modifiers and constraints to imported objects even if they are not animated so they can be updated when reloading the Alembic archive')

    # Universal Scene Description
    bpy.types.Scene.usd_dt_camera = bpy.props.BoolProperty(name='Cameras', default=True)
    bpy.types.Scene.usd_dt_curves = bpy.props.BoolProperty(name='Curves', default=True)
    bpy.types.Scene.usd_dt_lights = bpy.props.BoolProperty(name='Lights', default=True)
    bpy.types.Scene.usd_dt_materials = bpy.props.BoolProperty(name='Materials', default=True)
    bpy.types.Scene.usd_dt_meshes = bpy.props.BoolProperty(name='Meshes', default=True)
    bpy.types.Scene.usd_dt_volumes = bpy.props.BoolProperty(name='Volume', default=True)
    bpy.types.Scene.usd_path_mask = bpy.props.StringProperty(name='Path Mask', description='Import only the subset of the USD scene rooted at the given primitive')
    bpy.types.Scene.usd_scale = bpy.props.FloatProperty(name='Scale', description='Value by which to enlarge or shrink the objects with respect to the worlds origin')
    bpy.types.Scene.usd_md_uv_coords = bpy.props.BoolProperty(name='UV Coordinates', description='Read mesh UV coordinates', default=True)
    bpy.types.Scene.usd_md_vertex_colors = bpy.props.BoolProperty(name='Vertex Colors', description='Read mesh vertex colors')
    bpy.types.Scene.usd_md_incl_subdivision = bpy.props.BoolProperty(name='Visible Primitives Only', description='')
    bpy.types.Scene.usd_md_incl_import_instance_proxies = bpy.props.BoolProperty(name='Import Instance Proxies', description='Create unique Blender objects for USd instances', default=True)
    bpy.types.Scene.usd_md_incl_visible_primitives_only = bpy.props.BoolProperty(name='Visible primitives only', description='Do not import invisible USD primitives. Only applies to primitives with a non-animated visibility attribute. Primitives with animated visibility will always be imported', default=True)
    bpy.types.Scene.usd_md_incl_guide = bpy.props.BoolProperty(name='Guide', description='Import guide geometry')
    bpy.types.Scene.usd_md_incl_proxy = bpy.props.BoolProperty(name='Proxy', description='Import proxy geometry', default=True)
    bpy.types.Scene.usd_md_incl_render = bpy.props.BoolProperty(name='Render', description='Import final render geometry', default=True)
    bpy.types.Scene.usd_md_opt_set_frame_range = bpy.props.BoolProperty(name='Set Frame range', description='Update the scenes start and end frame to match those of hte USD archive', default=True)
    bpy.types.Scene.usd_md_opt_relative_path = bpy.props.BoolProperty(name='Relative Path', description='Select the file relative to the blend file', default=True)
    bpy.types.Scene.usd_md_opt_collection = bpy.props.BoolProperty(name='Create Collection', description='Add all objects to a new collection')
    bpy.types.Scene.usd_md_light_intensity_scale = bpy.props.FloatProperty(name='Light Intensity Scale', description='Scale for the intensity of imported lights', default=1)
    bpy.types.Scene.usd_md_exp_import_usd_preview = bpy.props.BoolProperty(name='Import USD Preview', description='Convert UsdPreviewSurface shaders to Principled BSDF shader networks')
    bpy.types.Scene.usd_md_exp_set_material_blend = bpy.props.BoolProperty(name='Set Material Blender', description='If the Import USD Preview option is enabled, the material blender method will automatically be set based on the shaders opacity and opacityThreshold inputs', default=True)

    # Import SVG as Grease Pencil
    bpy.types.Scene.svg_gp_resolution = bpy.props.IntProperty(name='Resolution', description='Resolution of the generated strokes', default=10)
    bpy.types.Scene.svg_gp_scale = bpy.props.FloatProperty(name='Scale', description='Scale of the final strokes', default=10.0)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(view3d_menu_add)
    bpy.types.VIEW3D_MT_add.remove(view3d_menu_add)

    bpy.utils.unregister_class(TEST_OT_ImportSomeData)
    bpy.utils.unregister_class(WM_OT_ImportCollada)
    bpy.utils.unregister_class(WM_OT_ImportAlembic)
    bpy.utils.unregister_class(WM_OT_ImportUniversalSceneDescription)
    bpy.utils.unregister_class(WM_OT_ImportSVGAsGreasePencil)


if __name__ == "__main__":
    register()