import numpy as np
import pickle
print("original")
with open("video/video_v_16.pickle", 'rb') as file:
    print(pickle.load(file))
print("rel")
with open("video/rel_video_16.pickle", 'rb') as file:
    print(pickle.load(file))
print("dff")
with open("video/dff_video_16.pickle", 'rb') as file:
    print(pickle.load(file))