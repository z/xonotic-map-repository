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

    entities_list = entities_dict.keys()

    entities = {
        'item_health_small': [],
        'item_health_medium': [],
        'item_health_large': [],
        'item_health_mega': [],

        'item_armor_small': [],
        'item_armor_medium': [],
        'item_armor_large': [],
        'item_armor_mega': [],

        'weapon_electro': [],
        'weapon_crylink': [],
        'weapon_vortex': [],
        'weapon_shotgun': [],
        'weapon_devastator': [],
        'weapon_grenadelauncher': [],
        'weapon_hagar': [],
        'weapon_arc': [],
        'weapon_machinegun': [],

        'item_flag_team1': [],
        'item_flag_team2': [],
        'item_flag_team3': [],
        'item_flag_team4': [],

        'item_shells': [],
        'item_bullets': [],
        'item_cells': [],
        'item_rockets': [],

        'info_player_deathmatch': [],
        'info_player_team1': [],
        'info_player_team2': [],
        'info_player_team3': [],
        'info_player_team4': [],
    }

    x0, x1, y0, y1 = get_map_boundaries(path_bsp + bsp_name + '/maps/' + bsp_name + '.bsp')

    #aspect = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 512
    #longest = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 2

    fig, ax = plt.subplots()
    plt.figure(figsize=(6, 6), dpi=96)
    plt.axis('off')

    map_entities = parse_entity_file(entities_file)

    symbol = entity_symbol
    color = entity_color
    size = entity_size

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

    for entity_type in entities:
        if entity_type in plot_entities_list:
            if entities[entity_type]:
                plot_it(entities[entity_type], symbol[entity_type], color[entity_type], int(size[entity_type]))

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
