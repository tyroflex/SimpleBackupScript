from math import floor
from math import log
from math import pow


def convert_size(size_byte):
    if size_byte == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(floor(log(size_byte, 1024)))
    p = pow(1024, i)
    s = round(size_byte/p, 2)
    return "{bsize} {unit}".format(bsize=s, unit=size_name[i])
