import os

from bpy import context
scene = context.scene

path = "/home/jappie/Videos/C/"
path = input("folder > ")
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

scene.frame_end = last_end
