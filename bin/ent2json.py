#!/usr/bin/env python3
# Description: Attempt to convert the entities JSON to valid JSON
# Author: Tyler "-z-" Mulligan

import json
import re

def replace_last(s, old, new):
    return s[::-1].replace(old[::-1], new[::-1], 1)[::-1]

in_file = 'resources/entities/gasoline_02.ent'
#in_file = 'resources/entities/vapor_alpha_2.ent'
out_file = 'test.json'

f = open(in_file, 'r')
file_data = f.read()
f.close()

file_data = re.sub(r'(".*") (".*")', r'\1: \2,', file_data)
file_data = re.sub(r'(".*": ".*"),\n}', r'\1\n},', file_data)

entities_list = [file_data]
#print(entities_list)
file_data = replace_last(file_data, '},', '}')
entities = json.loads("[" + file_data + "]")

#print(entities)

entities_health = []
entities_armor = []
entities_weapon = []
entities_ammo = []
entities_spawn = []
entities_other = []

for e in entities:
    if 'origin' in e:
        classname = e['classname']
#        print(classname)
        origin = e['origin'].split()
        origin.pop()
        xy = tuple(origin)
#        print(xy)

        if re.match(r'^item_health', classname):
            entities_health.append(xy)

        if re.match(r'^item_armor', classname):
            entities_armor.append(xy)

        if re.match(r'^weapon_', classname):
            entities_weapon.append(xy)

        if re.match(r'^item_(bullets|rockets|cell|shells|plasma)', classname):
            entities_ammo.append(xy)

        if re.match(r'^info_player', classname):
            entities_spawn.append(xy)


from matplotlib import pyplot as plt
import numpy as np
import matplotlib

#radar_image = 'resources/radars/gfx/vapor_alpha_2_mini.png'
#radar_image = 'resources/radars/gfx/gasoline_02_mini.png'
radar_image = 'gasoline_02_radar.png'
#radar_image = 'space-elevator_radar.png'
#radar_image = 'stinkbug.png'

fig = plt.figure(figsize=(6, 6), dpi=96)
#fig = plt.figure()
ax = fig.add_subplot(111)
plt.axis('off')


def plot_it(zipped, marker, color):

    x, y = zip(*zipped)
    s = [10]

    plt.scatter(x, y, s, c=color, alpha=0.5, marker=marker)

if entities_health:
    plot_it(entities_health, 'o', "r")

if entities_armor:
    plot_it(entities_armor, 'o', "g")

if entities_weapon:
    plot_it(entities_weapon, 'o', "b")

if entities_ammo:
    plot_it(entities_weapon, 'o', "gray")

if entities_spawn:
    plot_it(entities_spawn, 'o', "w")

print(entities_health)

# Remove margins
plot_margin = 0
#x0, x1, y0, y1 = plt.axis()

# add image
img = plt.imread(radar_image)

x0 = -1544
x1 = 1544
y0 = -3592
y1 = 6664

plt.axis((x0 - plot_margin,
          x1 + plot_margin,
          y0 - plot_margin,
          y1 + plot_margin))
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

aspect = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 512

print(aspect)

x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()

#ax.imshow(img, extent=[x0, x1, y0, y1])

longest = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 2

#ax.imshow(img, extent=[-longest, longest, -longest, longest])
#plt.imshow(img, extent=[-longest, longest, -longest, longest])
#ax.imshow(img, extent=[y0, y1, x0, x1], origin='upper')
#plt.imshow(img)

plt.axes().set_aspect('equal', 'datalim')
plt.show()
fig.canvas.draw()


plt.savefig("test.png", transparent=True)


#f = open(out_file, 'w')
#f.write(json.dumps(entities))
#f.close()
