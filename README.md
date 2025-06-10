# AutoWalker – Blender Plugin

AutoWalker is a Blender plugin designed to automatically add movement to walk or run animations. It simplifies the process of animating forward motion for characters based on existing walk/run cycles. Just specify the bones, animation range, and a target object to generate a natural walk path.

## Features
Automatically adds forward movement to looping walk/run animations.

Supports custom foot and root bones.

Set custom animation frame ranges.

Use target objects (like Empties) as the destination for your character's movement.

Simple UI integrated into Blender's side panel.

## Installation
Download the plugin .zip file.

Open Blender and go to Edit > Preferences > Add-ons.

Click Install, select the downloaded file, and click Install Add-on.

Enable the add-on by checking the box next to its name.

## How to Use
- Foot Bone: Enter the name of the foot bone used in your walk cycle (e.g., R_Foot).

- Root Bone: Enter the name of the armature’s root bone (e.g., Root).

- Head / Tail: Pick where to get the location data from bones(Default Head should work if you have any issues you can switch to Tail).

- Start Frame / End Frame: Set the frame range for the walk or run cycle.

- Start Point / End Point: Pick if the movement starts or ends at the original point.

- Target Object: Choose an Empty or another object to define the direction and distance of the movement if nothing is selected it will apply to armature itself.

- Click Auto Walk to apply movement.

## License
MIT License. Use freely in personal and commercial projects.