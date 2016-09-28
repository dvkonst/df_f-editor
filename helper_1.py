import numpy as np
from tifffile import TiffFile
# '''
with TiffFile('video/CA1_10_20160915_151232.tif_cropped.tif') as tif:
    # print(tif.pages, tif.size, sep='\n')
    print(tif.__len__(), type(tif.__len__()))
    # print(tif.__str__(), type(tif.__str__()))
    print(tif.filename)
    pass
# '''
# '''
files = open("*.txt")
print(files)
# '''
print()
