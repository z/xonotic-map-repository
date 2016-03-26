#!/usr/bin/env python3
# Description: Plots entities on radars
# Author: Tyler "-z-" Mulligan

from matplotlib import pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as font_manager
import struct
import sys
import os
from entities2json import *
from entities import *


path_entities = 'resources/entities/'
path_radar = 'resources/radars/gfx/'
path_bsp = 'resources/bsp/'


def main():

    bsp_name = sys.argv[1]

    entities_file = path_entities + bsp_name + '.ent'
    radar_image = path_radar + bsp_name + '_mini.png'

    map_entities = parse_entity_file(entities_file)

    entities_list = entities_dict.keys()

    symbol = entity_symbol
    color = entity_color
    size = entity_size
    these = symbol.keys()
    entities = dict((k, []) for k in these)

    x0, x1, y0, y1 = get_map_boundaries(path_bsp + bsp_name + '/maps/' + bsp_name + '.bsp')

    #aspect = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 512
    #longest = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 2

    fig, ax = plt.subplots()
    plt.figure(figsize=(6, 6), dpi=96)
    plt.axis('off')

    for e in map_entities:
        if 'origin' in e:
            if e['classname'] in entities_list:
                classname = entities_dict[e['classname']]
                origin = e['origin'].split()
                origin.pop()
                xy = tuple(origin)
                
                if classname in entities:
                    entities[classname].append(xy)

    plot_entities_list = entities.keys()

    for classname in entities:
        if classname in plot_entities_list:
            if entities[classname]:
                plot_it(entities[classname], symbol[classname], color[classname], int(size[classname]))

    # add image
    img = plt.imread(radar_image)
    plt.imshow(img, extent=[x0, x1, y0, y1], origin='upper', aspect='auto')

    plt.axes().set_aspect('equal', 'datalim')
    plt.show()
    fig.tight_layout()
    fig.canvas.draw()

    plt.savefig("resources/entities_maps/" + bsp_name + ".png", transparent=True, dpi=120)


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


def plot_it(zipped, symbol, color, scale):

    x, y = zip(*zipped)
    s = [scale]

    font_name = 'icomoon.ttf'
    path = os.path.join('static', 'css', 'fonts', font_name)
    prop = font_manager.FontProperties(fname=path)

    if symbol is 'o':
        plt.scatter(x, y, s, c=color, alpha=1, marker=symbol)
    else:
        for x0, y0 in zipped:
            plt.text(x0, y0, symbol, fontproperties=prop, size=scale, va='center', ha='center', clip_on=True, color=color)


if __name__ == "__main__":
    main()
