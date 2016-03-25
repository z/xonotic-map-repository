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
from entities import entities_dict


path_entities = 'resources/entities/'
path_radar = 'resources/radars/gfx/'
path_bsp = 'resources/bsp/'


def main():

    bsp_name = sys.argv[1]

    symbol_health_small = u'\uE913'
    symbol_health_medium = u'\uE914'
    symbol_health_large = u'\uE915'
    symbol_health_mega = u'\uE916'

    symbol_armor_small = u'\uE91b'
    symbol_armor_medium = u'\uE91a'
    symbol_armor_large = u'\uE919'
    symbol_armor_mega = u'\uE918'    

    symbol_electro = u'\ue926'
    symbol_crylink = u'\ue925'
    symbol_vortex = u'\ue931'
    symbol_shotgun = u'\ue938'
    symbol_devastator = u'\ue934'
    symbol_grenadelauncher = u'\ue929'
    symbol_hagar = u'\ue92a'
    symbol_arc = u'\ue924'
    symbol_machinegun = u'\ue93a'

    symbol_shells = u'\ue922'
    symbol_bullets = u'\ue91d'
    symbol_cells = u'\ue91e'
    symbol_rockets = u'\ue921'

    symbol_flag = u'\ue91c'

    entities_file = path_entities + bsp_name + '.ent'
    radar_image = path_radar + bsp_name + '_mini.png'

    entities_list = entities_dict.keys()

    x0, x1, y0, y1 = get_map_boundaries(path_bsp + bsp_name + '/maps/' + bsp_name + '.bsp')

    #aspect = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 512
    #longest = max(abs(x0) + abs(x1), abs(y0) + abs(y1)) / 2

    fig, ax = plt.subplots()
    plt.figure(figsize=(6, 6), dpi=96)
    plt.axis('off')

    entities = parse_entity_file(entities_file)

    # Make this whole section less verbose
    entities_health_small = []
    entities_health_medium = []
    entities_health_large = []
    entities_health_mega = []

    entities_armor_small = []
    entities_armor_medium = []
    entities_armor_large = []
    entities_armor_mega = []

    entities_electro = []
    entities_crylink = []
    entities_vortex = []
    entities_shotgun = []
    entities_devastator = []
    entities_grenadelauncher = []
    entities_hagar = []
    entities_arc = []
    entities_machinegun = []

    entities_flag_team1 = []
    entities_flag_team2 = []
    entities_flag_team3 = []
    entities_flag_team4 = []

    entities_shells = []
    entities_bullets = []
    entities_cells = []
    entities_rockets = []

    entities_spawn = []

    entities_other = []

    for e in entities:
        if 'origin' in e:
            if e['classname'] in entities_list:
                classname = entities_dict[e['classname']]
                origin = e['origin'].split()
                origin.pop()
                xy = tuple(origin)

                if classname is "item_health_small":
                    entities_health_small.append(xy)

                if classname is "item_health_medium":
                    entities_health_medium.append(xy)

                if classname is "item_health_large":
                    entities_health_large.append(xy)

                if classname is "item_health_mega":
                    entities_health_mega.append(xy)

                if classname is "item_armor_small":
                    entities_armor_small.append(xy)

                if classname is "item_armor_medium":
                    entities_armor_medium.append(xy)

                if classname is "item_armor_large":
                    entities_armor_large.append(xy)

                if classname is "item_armor_mega":
                    entities_armor_mega.append(xy)

                if classname is "weapon_devastator":
                    entities_devastator.append(xy)

                if classname is "weapon_electro":
                    entities_electro.append(xy)

                if classname is "weapon_crylink":
                    entities_crylink.append(xy)

                if classname is "weapon_vortex":
                    entities_vortex.append(xy)

                if classname is "weapon_shotgun":
                    entities_shotgun.append(xy)

                if classname is "weapon_devastator":
                    entities_devastator.append(xy)

                if classname is "weapon_grenadelauncher":
                    entities_grenadelauncher.append(xy)

                if classname is "weapon_hagar":
                    entities_hagar.append(xy)

                if classname is "weapon_arc":
                    entities_arc.append(xy)

                if classname is "weapon_machinegun":
                    entities_machinegun.append(xy)

                if classname is "item_shells":
                    entities_shells.append(xy)

                if classname is "item_bullets":
                    entities_bullets.append(xy)

                if classname is "item_cells":
                    entities_cells.append(xy)

                if classname is "item_rockets":
                    entities_rockets.append(xy)

                if classname is "item_flag_team1":
                    entities_flag_team1.append(xy)

                if classname is "item_flag_team2":
                    entities_flag_team2.append(xy)

                if classname is "item_flag_team3":
                    entities_flag_team3.append(xy)

                if classname is "item_flag_team4":
                    entities_flag_team4.append(xy)

                if classname is "info_player":
                    entities_spawn.append(xy)

    # Health
    if entities_health_small:
        plot_it(entities_health_small, symbol_health_small, "red", 10)

    if entities_health_medium:
        plot_it(entities_health_medium, symbol_health_medium, "red", 10)

    if entities_health_large:
        plot_it(entities_health_large, symbol_health_large, "red", 10)

    if entities_health_mega:
        plot_it(entities_health_mega, symbol_health_mega, "red", 10)

    # Armor
    if entities_armor_small:
        plot_it(entities_armor_small, symbol_armor_small, "green", 10)

    if entities_armor_medium:
        plot_it(entities_armor_medium, symbol_armor_medium, "green", 10)

    if entities_armor_large:
        plot_it(entities_armor_large, symbol_armor_large, "green", 10)

    if entities_armor_mega:
        plot_it(entities_armor_mega, symbol_armor_mega, "green", 10)

    # Weapons
    if entities_devastator:
        plot_it(entities_devastator, symbol_devastator, "#ECD262", 10)

    if entities_electro:
        plot_it(entities_electro, symbol_electro, "#69A0E7", 10)

    if entities_crylink:
        plot_it(entities_crylink, symbol_crylink, "#F580F7", 10)

    if entities_vortex:
        plot_it(entities_vortex, symbol_vortex, "#73BACA", 10)

    if entities_shotgun:
        plot_it(entities_shotgun, symbol_shotgun, "#95AFBE", 10)

    if entities_grenadelauncher:
        plot_it(entities_grenadelauncher, symbol_grenadelauncher, "pink", 10)

    if entities_hagar:
        plot_it(entities_hagar, symbol_hagar, "#FFA789", 10)

    if entities_arc:
        plot_it(entities_arc, symbol_arc, "#C3EEFF", 10)

    if entities_machinegun:
        plot_it(entities_machinegun, symbol_machinegun, "#8CE54A", 10)

    # Ammo
    if entities_shells:
        plot_it(entities_shells, symbol_shells, "#BECBD3", 6)

    if entities_bullets:
        plot_it(entities_bullets, symbol_bullets, "#B1D887", 6)

    if entities_rockets:
        plot_it(entities_rockets, symbol_rockets, "#E1B08D", 6)

    if entities_cells:
        plot_it(entities_cells, symbol_cells, "#B1FFFF", 6)

    # Flags
    if entities_flag_team1:
        plot_it(entities_flag_team1, symbol_flag, "#FF0000", 10)

    if entities_flag_team2:
        plot_it(entities_flag_team2, symbol_flag, "#0080FF", 10)

    if entities_flag_team3:
        plot_it(entities_flag_team3, symbol_flag, "pink", 10)

    if entities_flag_team4:
        plot_it(entities_flag_team4, symbol_flag, "yellow", 10)

    # Players
    if entities_spawn:
        plot_it(entities_spawn, 'o', "orange", 30)

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

    fontname = 'icomoon.ttf'

    path = os.path.join('static', 'css', 'fonts', fontname)

    prop = font_manager.FontProperties(fname=path)

    if symbol is 'o':
        plt.scatter(x, y, s, c=color, alpha=1, marker=symbol)
    else:
        for x0, y0 in zipped:
            plt.text(x0, y0, symbol, fontproperties=prop, size=scale, va='center', ha='center', clip_on=True, color=color)


if __name__ == "__main__":
    main()
