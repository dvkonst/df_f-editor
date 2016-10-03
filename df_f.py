import numpy as np
import sys
import os
import glob
from timer import Timer
from tifffile import TiffFile, TiffWriter, TiffSequence


def main():
    with Timer() as time_all_files_for_max_min:
        path = "video_in"
        files = glob.glob(os.path.join(path, '*.tif'))
        sum_pages_list = []
        min_list = []
        max_list = []
        for file_name in files:
            print("begin", file_name)
            with Timer() as time_video, TiffFile(file_name) as full_file:
                name = full_file.filename
                formats = str(full_file[-1]).split(": ")[1].split(", ")
                num_pages = full_file.__len__()
                size_pages = np.array(formats[0].split(" x "), dtype=np.uint16)
                flat_len = np.prod(size_pages)
                size_pix = int(formats[2].split(' ')[0])
                max_uint16 = 2 ** size_pix
                n_iter = range(num_pages)
                del formats
                # print("egegey")
                with Timer() as time_sum:
                    sum_pages = np.zeros(size_pages, dtype=np.uint32)
                    for n in n_iter:
                        sum_pages += full_file[n].asarray()
                    for i in range(flat_len):
                        if sum_pages.flat[i] == 0:
                            sum_pages.flat[i] = 1
                    sum_pages_list.append(sum_pages)
                print("time sum", time_sum.secs)

                with Timer() as time_rel:
                    rel_kdr_max = np.vectorize(lambda n: np.amax(np.true_divide(full_file[n].asarray(), sum_pages)))
                    rel_kdr_min = np.vectorize(lambda n: np.amin(np.true_divide(full_file[n].asarray(), sum_pages)))
                    min_list.append(np.amin(rel_kdr_min(n_iter)))
                    max_list.append(np.amax(rel_kdr_max(n_iter)))
                print("time_rel", time_rel.secs)
                # del new_sum_pages
            print("time_video", time_video.secs)
            print()
        min_val, max_val = min(min_list), max(max_list)
        const_1 = max_uint16 / (max_val - min_val)
        print(min_val, max_val)
        j = 0
        for file_name in files:
            print("begin round")
            with Timer() as time_round, TiffFile(file_name) as full_file:
                name = full_file.filename
                with TiffWriter('video_out/' + name, bigtiff=True) as tif:
                    num_pages = full_file.__len__()
                    n_iter = range(num_pages)
                    for n in n_iter:
                        tif.save((np.around(
                            np.multiply(np.subtract(np.true_divide(
                                full_file[n].asarray(), sum_pages_list[j]), min_val), const_1))
                                ).astype(np.uint16))
            j += 1
            print("time_round", time_round.secs)

    print("time_all_files_for_max_min", time_all_files_for_max_min.secs / 60, "minutes")
# params = {"num_pages": num_pages, "size_pages": size_pages, "pix_type": pix_type, "size_pix": size_pix}
# tif.save((np.around(fullfile[n].asarray() * const_1 /
#                     (sum_pages * max_value))).astype(np.uint16))
if __name__ == '__main__':
    sys.exit(main())
