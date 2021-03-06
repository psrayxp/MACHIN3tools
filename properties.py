import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, CollectionProperty, PointerProperty, EnumProperty, FloatProperty


# COLLECTIONS

class AppendMatsCollection(bpy.types.PropertyGroup):
    name: StringProperty()


class HistoryObjectsCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    obj: PointerProperty(name="History Object", type=bpy.types.Object)


class HistoryUnmirroredCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    obj: PointerProperty(name="History Unmirror", type=bpy.types.Object)


class HistoryEpochCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    objects: CollectionProperty(type=HistoryObjectsCollection)
    unmirrored: CollectionProperty(type=HistoryUnmirroredCollection)


# SCENE PROPERTIES


class M3SceneProperties(bpy.types.PropertyGroup):
    def update_pass_through(self, context):
        shading = context.space_data.shading

        shading.show_xray = self.pass_through
        shading.xray_alpha = 1 if context.active_object and context.active_object.type == "MESH" else 0.5

    def update_show_edit_mesh_wire(self, context):
        shading = context.space_data.shading

        shading.show_xray = self.show_edit_mesh_wire
        shading.xray_alpha = 0.1

    def update_uv_sync_select(self, context):
        toolsettings = context.scene.tool_settings
        toolsettings.use_uv_select_sync = self.uv_sync_select

        if not toolsettings.use_uv_select_sync:
            bpy.ops.mesh.select_all(action="SELECT")

    def update_eevee_gtao_factor(self, context):
        context.scene.eevee.gtao_factor = self.eevee_gtao_factor

    def update_show_cavity(self, context):
        t = (self.show_cavity, self.show_curvature)
        shading = context.space_data.shading

        shading.show_cavity = True if any(t) else False

        if t == (True, True):
            shading.cavity_type = "BOTH"

        elif t == (True, False):
            shading.cavity_type = "WORLD"

        elif t == (False, True):
            shading.cavity_type = "SCREEN"

    def update_show_curvature(self, context):
        t = (self.show_cavity, self.show_curvature)
        shading = context.space_data.shading

        shading.show_cavity = True if any(t) else False

        if t == (True, True):
            shading.cavity_type = "BOTH"

        elif t == (True, False):
            shading.cavity_type = "WORLD"

        elif t == (False, True):
            shading.cavity_type = "SCREEN"

    pass_through: BoolProperty(name="Pass Through", default=False, update=update_pass_through)
    show_edit_mesh_wire: BoolProperty(name="Show Edit Mesh Wireframe", default=False, update=update_show_edit_mesh_wire)
    uv_sync_select: BoolProperty(name="Synce Selection", default=False, update=update_uv_sync_select)
    eevee_gtao_factor: FloatProperty(name="Factor", default=1, min=0, update=update_eevee_gtao_factor)

    show_cavity: BoolProperty(name="Cavity", default=True, update=update_show_cavity)
    show_curvature: BoolProperty(name="Curvature", default=False, update=update_show_curvature)

    focus_history: CollectionProperty(type=HistoryEpochCollection)
