#!/usr/bin/env python3
# Description: Plots entities on radars
# Author: Tyler "-z-" Mulligan

from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import struct
import sys
from entities2json import *

path_entities = 'resources/entities/'
path_radar = 'resources/radars/gfx/'
path_bsp = 'resources/bsp/'


def main():

    bsp_name = sys.argv[1]

    entities_file = path_entities + bsp_name + '.ent'

    entities = parse_entity_file(entities_file)

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


    radar_image = path_radar + bsp_name + '_mini.png'
    #radar_image = 'gasoline_02_radar.png'
    #radar_image = 'resources/radars/gfx/vapor_alpha_2_mini.png'
    #radar_image = 'resources/radars/gfx/gasoline_02_mini.png'
    #radar_image = 'space-elevator_radar.png'
    #radar_image = 'stinkbug.png'

    fig = plt.figure(figsize=(6, 6), dpi=96)
    #fig = plt.figure()
    #ax = fig.add_subplot()
    #fig, ax = plt.subplots()
    #plt.axis('off')

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

    x0, x1, y0, y1 = get_map_boundaries(path_bsp + bsp_name + '/maps/' + bsp_name + '.bsp')

    # x0 = -1544
    # x1 = 1544
    # y0 = -3592
    # y1 = 6664

    aspect = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 512
    longest = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 2

    #print(aspect, longest)

    # add image
    img = plt.imread(radar_image)

    # Remove margins
    plot_margin = 0
    plt.axis((x0 - plot_margin,
              x1 + plot_margin,
              y0 - plot_margin,
              y1 + plot_margin))
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    #x0, x1 = ax.get_xlim()
    #y0, y1 = ax.get_ylim()

    #ax.imshow(img, extent=[x0, x1, y0, y1])

    #plt.imshow(img, extent=[-(longest), longest, -(longest), longest], origin='lower')
    #plt.imshow(img, extent=[-longest, longest, -longest, longest])
    plt.imshow(img, extent=[x0, x1, y0, y1], origin='upper')
    #plt.imshow(img)

    plt.axes().set_aspect('equal', 'datalim')
    plt.show()
    fig.tight_layout()
    fig.canvas.draw()

    #plt.savefig("test.png", transparent=True)

    plt.savefig("test.png", transparent=True, dpi=85.4)


def get_map_boundaries(bsp_file):

    f = open(bsp_file, 'rb')
    f.seek(32)
    bytes = f.read(4)
    next_int = struct.unpack('i', bytes)
    f.seek(next_int[0] + 12)

    bytes = f.read(12)
    min_coords = struct.unpack('iii', bytes)

    bytes = f.read(12)
    max_coords = struct.unpack('iii', bytes)

    min_x, min_y, min_z = min_coords
    max_x, max_y, max_z = max_coords

    return min_x, max_x, min_y, max_y


def plot_it(zipped, marker, color):

    x, y = zip(*zipped)
    s = [10]

    plt.scatter(x, y, s, c=color, alpha=0.5, marker=marker)


if __name__ == "__main__":
    main()
