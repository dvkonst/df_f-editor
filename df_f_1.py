import numpy as np
import pickle
# import

with open("video_params.txt", 'r') as params:
    """
    reading parameters of video from file
    """
    Pixel_type = np.uint16
    max_pixel_value = 65536
    str_num = 2
    col_num = 2
    kdr_num = 2
    files_num = 2
    all_kdr_num = files_num * kdr_num

Sum_kdr = np.zeros((kdr_num, str_num, col_num), dtype=np.uint32)
iter_files = range(files_num)
for n in iter_files:
    with open("video_" + str(n) + ".pickle", 'rb') as file:
        part_video = pickle.load(file)
        Sum_kdr += np.sum(part_video, axis=0, keepdims=True)
    del part_video
print("sum counted")
Max_rel_pix = 0
for n in iter_files:
    with open("video_" + str(n) + ".pickle", 'rb') as file:
        part_video = pickle.load(file)
        Rel_part_video = all_kdr_num * part_video / Sum_kdr
        condlist = Rel_part_video > 0.1
        choiselist = Rel_part_video
        Rel_part_video = np.select(condlist, choiselist)
        del part_video
    # temp_file_name = "rel_video_" + str(n) + ".pickle"
    with open("rel_video_" + str(n) + ".pickle", 'wb') as temp_file:
        pickle.dump(Rel_part_video, temp_file)
    Max_rel_pix = max(Max_rel_pix, np.amax(Rel_part_video))
    del Rel_part_video
for n in iter_files:
    with open("rel_video_" + str(n) + ".pickle", 'rb') as temp_file:
        Rel_part_video = pickle.load(temp_file)
    Df_f_part_video = (np.rint(Rel_part_video * max_pixel_value / Max_rel_pix)).astype(Pixel_type)
    with open("dff_video_" + str(n) + ".pickle", 'wb') as res_file:
        pickle.dump(Df_f_part_video, res_file)
    del Df_f_part_video