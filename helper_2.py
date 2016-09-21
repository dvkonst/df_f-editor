import numpy as np
import pickle
from timer import Timer
# import libtiff
import imread
# """
from tifffile import TiffFile
with TiffFile('video/CA1_10_20160915_151232.tif_cropped.tif') as tif:
    # images = tif.asarray()
    # for page in tif:
    #     for tag in page.tags.values():
    #         t = tag.name, tag.value
    #     image = page.asarray()
    with Timer() as t:
        print(str(tif[-1]))
    print(t.msecs)
# """
# from PIL import Image
# im = Image.open('video/CA1_10_20160915_151232.tif_cropped.tif')
# im.show()
# imarray = np.array(im)
# print(imarray.shape)
"""
tif = TIFF.open('video/CA1_10_20160915_151232.tif_cropped.tif', mode='r')
for image in tif.iter_images():
    print(image)
    input()
# """

# imread.imread_multi('video/CA1_10_20160915_151232.tif_cropped.tif')