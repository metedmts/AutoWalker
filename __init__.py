bl_info = {
    "name": "Auto Walker",
    "author": "metevfx",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "description": "An addon to automaticly add position keyframes to walk cycles"
}

import bpy
from bpy.utils import register_class, unregister_class
from .movement import AddMovement

class ObjectPickerProperties(bpy.types.PropertyGroup):
    target_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Target Object",
        description="Select an object from the scene"
    )

class TypeProperties(bpy.types.PropertyGroup):
    my_choice: bpy.props.EnumProperty(
        name="Type",
        description="Choose between two options",
        items=[
            ('START POINT', "Start Point", "Starts the movement from this location"),
            ('END POINT', "End Point", "Ends the movement at this location"),
        ],
        default='START POINT' 
    )

class BoneProperties(bpy.types.PropertyGroup):
    my_choice: bpy.props.EnumProperty(
        name="BonePos",
        description="Choose between two options",
        items=[
            ('HEAD', "Head", "Gets the head position"),
            ('TAIL', "Tail", "Gets the tail position"),
        ],
        default='HEAD' 
    )

class AutoWalkPanel(bpy.types.Panel):
    bl_label = "AutoWalker"
    bl_idname = "anim.auto_walk"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Auto Walk"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        type_of_movement = scene.type
        t_object = scene.target_object

        bone_pos = scene.bone_pos

        box = layout.box()
        box.prop(scene, "foot_bone", text="Foot Bone")
        box.prop(scene, "root_bone", text="Root Bone")

        box.prop(bone_pos, "my_choice", expand=True)

        box.prop(scene, "start_frame", text="Start Frame")
        box.prop(scene, "end_frame", text="End Frame")

        box.prop(type_of_movement, "my_choice", expand=True)

        box.prop(t_object, "target_object")

        box.operator(AddMovement.bl_idname, text=AddMovement.bl_label)

_classes = [
    AutoWalkPanel,
    AddMovement,
    TypeProperties,
    ObjectPickerProperties,
    BoneProperties
]

def register():
    for cls in _classes:
        register_class(cls)
    
    bpy.types.Scene.start_frame = bpy.props.IntProperty(name="Start Frame")
    bpy.types.Scene.end_frame = bpy.props.IntProperty(name="Start Frame")
    bpy.types.Scene.foot_bone = bpy.props.StringProperty(name="Foot Bone")
    bpy.types.Scene.root_bone = bpy.props.StringProperty(name="Root Bone", default="Root")
    bpy.types.Scene.type = bpy.props.PointerProperty(type=TypeProperties)
    bpy.types.Scene.target_object = bpy.props.PointerProperty(type=ObjectPickerProperties)
    bpy.types.Scene.bone_pos = bpy.props.PointerProperty(type=BoneProperties)

def unregister():
    for cls in _classes:
        unregister_class(cls)

    del bpy.types.Scene.start_frame
    del bpy.types.Scene.end_frame
    del bpy.types.Scene.foot_bone
    del bpy.types.Scene.root_bone
    del bpy.types.Scene.type
    del bpy.types.Scene.target_object
    del bpy.types.Scene.bone_pos


if __name__ == "__main__":
    register()