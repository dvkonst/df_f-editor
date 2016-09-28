import numpy as np
import sys
import os
import glob
from timer import Timer
from tifffile import TiffFile, TiffWriter, TiffSequence


def main():
    with Timer() as time_all_files:
        path = "video_in"
        for file_name in glob.glob(os.path.join(path, '*.tif')):
            print("begin", file_name)
            with Timer() as time_video, TiffFile(file_name) as full_file:
                name = full_file.filename
                formats = str(full_file[-1]).split(": ")[1].split(", ")
                num_pages = full_file.__len__()
                size_pages = np.array(formats[0].split(" x "), dtype=np.uint16)
                size_pix = int(formats[2].split(' ')[0])
                max_uint16 = 2 ** size_pix
                n_iter = range(num_pages)
                del formats
                # print("egegey")
                with Timer() as time_sum:
                    sum_pages = np.ones(size_pages, dtype=np.uint32)
                    for n in n_iter:
                        sum_pages += full_file[n].asarray()
                print("time sum", time_sum.secs)

                with Timer() as time_rel:
                    rel_kdr = np.vectorize(lambda n: np.amax(np.true_divide(full_file[n].asarray(), sum_pages)))
                    max_value = np.amax(rel_kdr(n_iter))
                print("time_rel", time_rel.secs)

                const_1 = max_uint16 / max_value
                new_sum_pages = np.multiply(np.reciprocal(sum_pages), const_1)
                del sum_pages

                with Timer() as time_round, TiffWriter('video_out/' + name, bigtiff=True) as tif:
                    for n in n_iter:
                        tif.save((np.around(full_file[n].asarray() * new_sum_pages)).astype(np.uint16))
                print("time_round", time_round.secs)
                # del new_sum_pages
            print("time_video", time_video.secs)
            print()
    print("time_all_files", time_all_files.secs / 60, "minutes")
# params = {"num_pages": num_pages, "size_pages": size_pages, "pix_type": pix_type, "size_pix": size_pix}
# tif.save((np.around(fullfile[n].asarray() * const_1 /
#                     (sum_pages * max_value))).astype(np.uint16))
if __name__ == '__main__':
    sys.exit(main())