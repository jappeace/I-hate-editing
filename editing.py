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
bl_info = {
    "name": "I-hate-editing",
    "category": "Import-Export",
}

import os

import bpy

def import_project(path, context):
    """Parse filenames and jam relevant files directly in the sequencer"""

    scene = context.scene

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
            print("%s: %i" % (imgfilename, len(range)))
            if len(range) <= 1:
                return False
            if int(range[0]) > int(desired_order):
                return False
            if range[1] == '':
                return True
            return int(desired_order) <= int(range[1])

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

# needs to be the same (read only)
_button_name = "project.importbutton"

class ImportProjectButton(bpy.types.Operator):
    """
    What happens when Quick Import is pressed
    1. first open the file selector dialogue.
    2. execute import project with the selected directory
    """
    bl_idname = _button_name
    bl_label = "quick import"
    directory = bpy.props.StringProperty(subtype="DIR_PATH")
 
    def execute(self, context):
        import_project(self.directory, context)
        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    """
    Tell blender how the menu item looks in a list.
    Note that in this case self becomes the list, 
    see the register function where this is used.
    Also attaches ImportProjectButton to this item because they share idname
    """
    self.layout.operator(_button_name, 
        text="Quick import", 
        icon='MESH_TORUS')
 
def register():
    """
    entry point
    Attaches menu function to the right list 
    (name can be found by hovering over items in blender)
    """
    bpy.utils.register_module(__name__)
    bpy.types.SEQUENCER_MT_add.prepend(menu_func)
 
def unregister():
    """Tell blender how to unload gracefully"""
    bpy.utils.unregister_module(__name__)
    bpy.types.SEQUENCER_MT_add.remove(menu_func)
 
if __name__ == "__main__":
    register()
