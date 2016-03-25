#!/usr/bin/env python3
# Author: Tyler "-z-" Mulligan

import struct

bsp_file = 'resources/map/gasoline_02.pk3_FILES/maps/gasoline_02.bsp'

f = open(bsp_file, 'rb')
f.seek(32)
bytes = f.read(4)
next_int = struct.unpack('i', bytes)
print(next_int)
f.seek(next_int[0] + 12)

bytes = f.read(12)
min_coords = struct.unpack('iii', bytes)

print(min_coords)

bytes = f.read(12)
max_coords = struct.unpack('iii', bytes)

print(max_coords)

min_x, min_y, min_z = min_coords
max_x, max_y, max_z = max_coords

print(min_x)
print(max_x)
print(min_y)
print(max_y)