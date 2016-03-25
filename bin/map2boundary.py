#!/usr/bin/env python3
# Author: Tyler "-z-" Mulligan

import re

in_file = 'resources/map/gasoline_02.pk3_FILES/maps/gasoline_02.map'

f = open(in_file, 'r')

limited_data = ""

for line in f:
    if re.search(r'\( [0-9-.]+ [0-9-.]+ [0-9-.]+ \) \( [0-9-.]+ [0-9-.]+ [0-9-.]+ \) \( [0-9-.]+ [0-9-.]+ [0-9-.]+ \) \( \(.*', line):
        limited_data += line

f.close()

new_data = re.sub(r'\( ([0-9-.]+) ([0-9-.]+) ([0-9-.]+) \) \( ([0-9-.]+) ([0-9-.]+) ([0-9-.]+) \) \( ([0-9-.]+) ([0-9-.]+) ([0-9-.]+) \) \( \(.*', r'(\1, \2, \3), (\4, \5, \6), (\7, \8, \9),', limited_data)

zipped = eval("[" + new_data + "]")

x, y, z = zip(*zipped)
x = list(x)
y = list(y)
z = list(z)

print(min(x))
print(max(x))

print(min(y))
print(max(y))
