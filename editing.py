# I hate editing jams your wav files and images automatically into the blender sequence editor
# Copyright (C) 2017 Jappie Klooster

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.If not, see <http:#www.gnu.org/licenses/>.


import os

import bpy
from bpy import context

def import_project():
    scene = context.scene

    path = "/home/jappie/Videos/C/"
    files = os.listdir(path)
    files.sort()

    # create the sequencer data
    scene.sequence_editor_create()
    seqs = scene.sequence_editor.sequences
    last_end = 1
    for (num, file) in enumerate([f for f in files if f.endswith('.wav')]):
        filename_parts = file.split('-')
        desired_order = filename_parts[0]

        seq = seqs.new_sound(
                name=str(file),
                filepath=os.path.join(path, file),
                channel=1, frame_start=last_end)

        def isInRange(imgfilename):
            range = imgfilename.split('-')[0].split('..')
            if len(range) <= 1:
                return False
            result = int(range[0]) <= int(desired_order) <= int(range[1])
            return result

        for (count, img) in enumerate([f for f in files if (f.startswith(desired_order) or isInRange(f)) and (f.endswith('.png') or f.endswith('.jpg'))]):
            imgseq = seqs.new_image(
                name=img,
                filepath=os.path.join(path, img),
                channel=count+2,
                frame_start=last_end,
            )
            imgseq.frame_final_end = seq.frame_final_end

        last_end = seq.frame_final_end

    print("blah")
    scene.frame_end = last_end
button_name = "project.importbutton"
class ImportProjectButton(bpy.types.Operator):
    bl_idname = button_name
    bl_label = "Say Hello"
 
    def execute(self, context):
        print("Hello world!")
        import_project()
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(button_name, 
        text="Quick import", 
        icon='MESH_TORUS')
 
def register():
   bpy.utils.register_module(__name__)
   bpy.types.SEQUENCER_MT_add.prepend(menu_func)
 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.SEQUENCER_MT_add.remove(menu_func)
 
if __name__ == "__main__":
    register()
