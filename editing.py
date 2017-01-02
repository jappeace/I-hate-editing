import os

from bpy import context
scene = context.scene

path = "/home/jappie/Videos/C/"
files = os.listdir(path)
files.sort()

# create the sequencer data
scene.sequence_editor_create()
seqs = scene.sequence_editor.sequences

last_end = 0
for (num, file) in enumerate([f for f in files if f.endswith('.wav')]):
    filename_parts = file.split('-')
    
    seq = seqs.new_sound(
            name=str(file),
            filepath=os.path.join(path, file),
            channel=1, frame_start=last_end)

    for (count, img) in enumerate([f for f in files if f.startswith(filename_parts[0]) and (f.endswith('.png') or f.endswith('.jpg'))]):
        imgseq = seqs.new_image(
            name=img,
            filepath=os.path.join(path, img),
            channel=count+2,
            frame_start=last_end,
        )


    last_end = seq.frame_final_end
# reverse if you want
seq.use_reverse_frames = False
