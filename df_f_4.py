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
                flat_len = np.prod(size_pages)
                size_pix = int(formats[2].split(' ')[0])
                max_uint16 = 2 ** (size_pix - 1)
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
                print("time sum", time_sum.secs)
                # print(sum_pages)
                # input()
                # print(1 / (sum_pages))

                with Timer() as time_rel:
                    rel_kdr_max = np.vectorize(lambda n: np.amax(np.true_divide(full_file[n].asarray(), sum_pages)))
                    rel_kdr_min = np.vectorize(lambda n: np.amin(np.true_divide(full_file[n].asarray(), sum_pages)))
                    max_value = np.amax(rel_kdr_max(n_iter))*num_pages
                    min_value = np.amax(rel_kdr_min(n_iter))*num_pages
                print("time_rel", time_rel.secs)
                print(min_value, max_value)

                with Timer() as time_round, TiffWriter('video_out/' + name, bigtiff=True) as tif:
                    c_1_one_min = max_uint16 / (1 - min_value)
                    c_1_max_one = max_uint16 / (max_value - 1)
                    c_max_two = max_value - 2
                    # for n in n_iter:
                    #     # part_video = (np.around(full_file[n].asarray() * new_sum_pages)).astype(np.uint16)
                    #     page = full_file[n].asarray().flat
                    #     s_page = sum_pages.flat
                    #     print(n)
                    #     for i in range(flat_len):
                    #         rel = page[i] / s_page[i] * num_pages
                    #         if rel <= 1:
                    #             r_page[i] = np.around((rel - min_value) * c_1_one_min * max_uint16)
                    #         else:
                    #             r_page[i] = np.around((rel + c_max_two) * c_1_max_one * max_uint16)
                    #     tif.save(res_page)
                    #     # print(part_video)

                    def func(n):
                        rel = np.multiply(np.true_divide(full_file[n].asarray(), sum_pages), num_pages)
                        tif.save(np.select([rel <= 1, rel > 1], [
                            (np.around(np.multiply(np.subtract(rel, min_value), c_1_one_min))).astype(np.uint16),
                            (np.around(np.multiply(np.add(rel, c_max_two), c_1_max_one))).astype(np.uint16)
                        ]))
                        # print(n)
                    np.vectorize(func)(n_iter)
                print("time_round", time_round.secs)

                # const_1 = max_uint16 / max_value
                # print(const_1)
                # new_sum_pages = np.multiply(1 / (sum_pages), const_1)
                # del sum_pages
                # print(new_sum_pages)
                # with Timer() as time_round, TiffWriter('video_out/' + name, bigtiff=True) as tif:
                #     for n in n_iter:
                #         part_video = (np.around(full_file[n].asarray() * new_sum_pages)).astype(np.uint16)
                #         tif.save(part_video)
                #         # print(part_video)
                # print("time_round", time_round.secs)
                # # del new_sum_pages
            print("time_video", time_video.secs)
            print()
    print("time_all_files", time_all_files.secs / 60, "minutes")
# params = {"num_pages": num_pages, "size_pages": size_pages, "pix_type": pix_type, "size_pix": size_pix}
# tif.save((np.around(fullfile[n].asarray() * const_1 /
#                     (sum_pages * max_value))).astype(np.uint16))
if __name__ == '__main__':
    sys.exit(main())