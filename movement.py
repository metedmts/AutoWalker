import bpy
import mathutils

def get_bone_relative_to_another_on_keyframes(armature_object, target_bone_name, reference_bone_name, start_keyframe, end_keyframe, location_type='head'):
    
    if armature_object.type != 'ARMATURE':
        print(f"Object '{armature_object.name}' is not an armature.")
        return None

    target_pose_bone = armature_object.pose.bones.get(target_bone_name)
    reference_pose_bone = armature_object.pose.bones.get(reference_bone_name)

    if not target_pose_bone:
        print(f"Target bone '{target_bone_name}' not found in armature '{armature_object.name}'.")
        return None
    if not reference_pose_bone:
        print(f"Reference bone '{reference_bone_name}' not found in armature '{armature_object.name}'.")
        return None
    
    if target_bone_name == reference_bone_name:
        print("Target bone and reference bone are the same.")
        return {frame: mathutils.Vector((0,0,0)) for frame in range(int(bpy.context.scene.frame_start), int(bpy.context.scene.frame_end) + 1)}

    original_frame = bpy.context.scene.frame_current

    relative_positions_at_keyframes = {}
    processed_positions_for_uniqueness = set()

    for frame in range(start_keyframe, end_keyframe+1):
        bpy.context.scene.frame_set(frame)

        bpy.context.view_layer.update()

        current_target_pose_bone = armature_object.pose.bones.get(target_bone_name)
        current_reference_pose_bone = armature_object.pose.bones.get(reference_bone_name)

        target_global_matrix = armature_object.matrix_world @ current_target_pose_bone.matrix
        reference_global_matrix = armature_object.matrix_world @ current_reference_pose_bone.matrix

        reference_global_inverse_matrix = reference_global_matrix.inverted()

        relative_transform_matrix = reference_global_inverse_matrix @ target_global_matrix

        relative_position = None 
        
        if location_type == 'head':
            relative_position = relative_transform_matrix.to_translation()
        elif location_type == 'tail':
            target_bone_data = armature_object.data.bones.get(target_bone_name) 
            if target_bone_data:
                target_tail_local_bone_space = mathutils.Vector((0, target_bone_data.length, 0)) 
                relative_position = relative_transform_matrix @ target_tail_local_bone_space
            else:
                print(f"Warning: Bone data for '{target_bone_name}' not found for tail calculation at frame {frame}.")
                continue 
        else:
            print("Invalid location_type. Use 'head' or 'tail'.")
            continue 

        if relative_position.freeze() in processed_positions_for_uniqueness: 
            break 
        
        relative_positions_at_keyframes[frame] = relative_position
        processed_positions_for_uniqueness.add(relative_position.freeze()) 

    bpy.context.scene.frame_set(original_frame)
    bpy.context.view_layer.update() 

    return relative_positions_at_keyframes

def add_to_active_object_position_along_local_axes_with_keyframes(obj, s,
    delta_x=0.0, delta_y=0.0, delta_z=0.0,
    original_pos_frame=1, new_pos_frame=10, e_p = False,
):
    if obj is None:
        s.report({"ERROR"}, "No active object selected.")
        return
    
    if obj.type != 'MESH' and obj.type != 'ARMATURE' and obj.type != 'EMPTY':
        s.report({"WARNING"}, f"Active object '{obj.name}' is of type '{obj.type}'. ")

    if original_pos_frame == new_pos_frame:
        s.report({"WARNING"}, "Original and new position keyframes are set to the same frame.")

    if obj.animation_data is None or obj.animation_data.action is None:
        obj.animation_data_create()
        walk_action = bpy.data.actions.new(name="Walk Movement")
        try:
            walk_slot = walk_action.slots.new(id_type="OBJECT", name="Walk Slot")
            obj.animation_data.action = walk_action
            obj.animation_data.action.slots.active = walk_slot
        except:
            obj.animation_data.action = walk_action

    x_curve = obj.animation_data.action.fcurves.find('location', index=0)
    if not x_curve:
        x_curve = obj.animation_data.action.fcurves.new('location', index=0)
    y_curve = obj.animation_data.action.fcurves.find('location', index=1)
    if not y_curve:
        y_curve = obj.animation_data.action.fcurves.new('location', index=1)
    z_curve = obj.animation_data.action.fcurves.find('location', index=2)
    if not z_curve:
        z_curve = obj.animation_data.action.fcurves.new('location', index=2)

    local_displacement = mathutils.Vector((delta_x, delta_y, delta_z))
    object_local_rotation = obj.matrix_local.to_quaternion()
    rotated_displacement_in_parent_space = object_local_rotation @ local_displacement

    original_scene_frame = bpy.context.scene.frame_current

    
    bpy.context.scene.frame_set(original_pos_frame)
    bpy.context.view_layer.update()

    if e_p == True:
        obj.location.x -= rotated_displacement_in_parent_space.x
        obj.location.y -= rotated_displacement_in_parent_space.y
        obj.location.z -= rotated_displacement_in_parent_space.z
    
    original_local_location = obj.location.copy()

    k1_x = x_curve.keyframe_points.insert(frame=original_pos_frame, value=obj.location.x)
    k1_y = y_curve.keyframe_points.insert(frame=original_pos_frame, value=obj.location.y)
    k1_z = z_curve.keyframe_points.insert(frame=original_pos_frame, value=obj.location.z)
    k1_x.interpolation = "LINEAR"
    k1_y.interpolation = "LINEAR"
    k1_z.interpolation = "LINEAR"

    print(f"Keyframed original position of '{obj.name}' at frame {original_pos_frame}: {original_local_location}")
    
    bpy.context.scene.frame_set(new_pos_frame)

    new_x = original_local_location.x + rotated_displacement_in_parent_space.x
    new_y = original_local_location.y + rotated_displacement_in_parent_space.y
    new_z = original_local_location.z + rotated_displacement_in_parent_space.z

    k2_x = x_curve.keyframe_points.insert(frame=new_pos_frame, value=new_x)
    k2_y = y_curve.keyframe_points.insert(frame=new_pos_frame, value=new_y)
    k2_z = z_curve.keyframe_points.insert(frame=new_pos_frame, value=new_z)
    k2_x.interpolation = "LINEAR"
    k2_y.interpolation = "LINEAR"
    k2_z.interpolation = "LINEAR"
    print(f"Keyframed new position of '{obj.name}' at frame {new_pos_frame}: {(new_x, new_y, new_z)}")

    bpy.context.scene.frame_set(original_scene_frame)
    bpy.context.view_layer.update()

class AddMovement(bpy.types.Operator):
    bl_idname = "anim.add_movement"
    bl_label = "Auto Walk"
    bl_description = "Adds the movement to walk animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object
        scene = context.scene
        target_bone_name = scene.foot_bone
        reference_bone_name = scene.root_bone
        type_of_movement = scene.type.my_choice
        bone_pos = scene.bone_pos.my_choice.lower()

        pos_count = {}
        pos_frames = {}
        highest = 0
        highest_key = ""
        try:
            target_name = scene.target_object.target_object.name
            target_obj = bpy.data.objects.get(target_name)
        except:
            target_obj = obj
        e_p = False
        if type_of_movement == 'END POINT':
            e_p = True
        if obj and obj.type == 'ARMATURE' and obj.animation_data:
            foot_relative_positions = get_bone_relative_to_another_on_keyframes(
                obj, target_bone_name, reference_bone_name, scene.start_frame, scene.end_frame, bone_pos
            )
            for frame, pos in foot_relative_positions.items():
                z_key = "{:.3f}".format(pos.z)
                print(f"Frame {frame}: {z_key}")
                try:
                    pos_count[z_key] += 1
                    pos_frames[z_key].append(frame)
                    if pos_count[z_key] > highest:
                        highest_key = z_key
                        highest = pos_count[z_key]
                except:
                    pos_count[z_key] = 1
                    pos_frames[z_key] = [frame]
                    if pos_count[z_key] > highest:
                        highest_key = z_key
                        highest = pos_count[z_key]
            print("Pos Count: ", pos_count)
            print("Pos Frames: ", pos_frames)
            print("Highest Key: ", highest_key)
            pos_change = foot_relative_positions[pos_frames[highest_key][0]] - foot_relative_positions[pos_frames[highest_key][-1]]
            vel = pos_change / (len(pos_frames[highest_key]) - 1)
            print("Velocity: ", vel)
            t = scene.end_frame - scene.start_frame
            add_to_active_object_position_along_local_axes_with_keyframes(target_obj, self, vel.x*t, vel.y*t, 0, scene.start_frame, scene.end_frame, e_p)
        
        return {'FINISHED'}