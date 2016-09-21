import numpy as np
import pickle
from timer import Timer
from tifffile import TiffFile
# import

# with open("video_params.txt", 'r') as params:
#     """
#     reading parameters of video from file
#     """
Pixel_type = np.uint16
max_pixel_value = 65536
pix_bytes = 2
str_num = 512
col_num = 512
# kdr_num = 16
n_num = 512
all_kdr_num = files_num * kdr_num
all_Gbytes = pix_bytes * str_num * col_num * all_kdr_num / 1024**3


def gen_video(n):
    with open('video/video_v_' + str(n) + '.pickle', 'wb') as file:
        pickle.dump(np.random.randint(65536, size=(kdr_num, str_num, col_num)).astype(np.uint16), file)
gen_video_V = np.vectorize(gen_video, [bool])
iter_files = range(files_num)
"""
with Timer() as t:
    gen_video_V(iter_files)
time = t.secs
# print(res.__sizeof__())
print("gen video", time, time / all_Gbytes)
# input()
# """
Sum_kdr = np.zeros((kdr_num, str_num, col_num), dtype=np.uint32)


def sum_video(n):
    global Sum_kdr
    with open("video/video_v_" + str(n) + ".pickle", 'rb') as file:
        Sum_kdr += np.sum(pickle.load(file), axis=0, keepdims=True)
sum_video_V = np.vectorize(sum_video, [bool])
print("sum() has begun")
with Timer() as t:
    sum_video_V(iter_files)
time = t.secs
print("sum", time, time / all_Gbytes)
print("sum counted")
print(Sum_kdr)
Max_rel_pix = 0.0


def rel_video(n):
    global Max_rel_pix
    with open("video/video_v_" + str(n) + ".pickle", 'rb') as file:
        Rel_part_video = pickle.load(file) * all_kdr_num / Sum_kdr
        # condlist = [Rel_part_video > 0.1]
        # choiselist = [Rel_part_video]
        # Rel_part_video = np.select(condlist, choiselist)
    # temp_file_name = "rel_video_" + str(n) + ".pickle"
    with open("video/rel_video_" + str(n) + ".pickle", 'wb') as temp_file:
        pickle.dump(Rel_part_video, temp_file)
    Max_rel_pix = max(Max_rel_pix, np.amax(Rel_part_video))
    del Rel_part_video
rel_video_V = np.vectorize(rel_video, [bool])
print("rel() has begun")
with Timer() as t:
    rel_video_V(iter_files)
time = t.secs
print("rel video", time, time / all_Gbytes)
print("rel video counted")
print("max", Max_rel_pix)
# input()
# """


def dff_video(n):
    global max_pixel_value, Max_rel_pix
    with open("video/rel_video_" + str(n) + ".pickle", 'rb') as temp_file:
        Df_f_part_video = (np.rint(pickle.load(temp_file) * max_pixel_value / Max_rel_pix)).astype(Pixel_type)
    with open("video/dff_video_" + str(n) + ".pickle", 'wb') as res_file:
        pickle.dump(Df_f_part_video, res_file)
    del Df_f_part_video

dff_video_V = np.vectorize(dff_video, [bool])
print("dff() has begun")
with Timer() as t:
    dff_video_V(iter_files)
time = t.secs
print("dff video", time, time / all_Gbytes)
print("dff video counted")
print("dff_example")
with open("video/dff_video_16.pickle", 'rb') as file:
    print(pickle.load(file))
print("rel_example")
with open("video/rel_video_16.pickle", 'rb') as file:
    print(pickle.load(file))
