import numpy as np
import pickle
from timer import Timer
# import libtiff
# import imread
# """
from tifffile import TiffFile
# pick = np.vectorize(lambda n: pickle.dump(tif[n].asarray(), open('video/v_' + str(n), 'wb')))
# close_files = np.vectorize(lambda n: )

with TiffFile('video/CA1_10_20160915_151232.tif_cropped.tif') as tif:
    # images = tif[0].asarray()

    # for page in tif:
    #     for tag in page.tags.values():
    #         t = tag.name, tag.value
    #     image = page.asarray()
    with Timer() as t:
        # pick(np.array(range(3000)))
        # sum_pages = np.zeros(, dtype=np.uint32)
        n_iter = range(3500)

        def sum_kdr(n):
            global sum_pages
            sum_pages += tif[n].asarray()
            return True
        sum_kdr = np.vectorize(sum_kdr)
        # sum_kdr = np.vectorize(lambda n: sum_pages += tif[n].asarray())
        sum_kdr(n_iter)
    print("time sum", t.secs)
    # print(sum_pages)
    with Timer() as t_:
        for x in np.nditer(sum_pages, op_flags=['readwrite']):
            if x == 0:
                x[...] += 1
    print("+1", t_.secs)
    with Timer() as tt:
        # rel_video = np.zeros()
        def rel_kdr(n):
            global sum_pages
            # print(np.sort(sum_pages))
            return np.amax(np.select([sum_pages != 0], [tif[n].asarray() / sum_pages], default=0))
        rel_kdr = np.vectorize(rel_kdr)
        print(np.amax(rel_kdr(n_iter)))
    print("time rel", tt.secs)

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

