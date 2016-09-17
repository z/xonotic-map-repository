#!/usr/bin/env python3
# Description: Loops through json generated by maps2json to download image urls
# Author: Tyler "-z-" Mulligan
import json
import os
import urllib.request
from xmr import util

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resources_dir = root_dir + '/resources/'
root_url = 'http://xonotic.co/resources/mapshots/'


def main():
    f = open(resources_dir + 'data/maps.json')
    data = f.read()
    maps_json = json.loads(data)['data']
    f.close()

    mapshots = []

    for m in maps_json:
        for bsp in m['bsp']:
            mapshots.append(m['bsp'][bsp]['mapshot'])

    unqiue_mapshots = list(set(mapshots))

    for m in unqiue_mapshots:
        if m != "":
            remote_image = root_url + m
            local_image = os.path.join(resources_dir + 'mapshots', m)
            print(remote_image)
            urllib.request.urlretrieve(remote_image, local_image, util.reporthook)


if __name__ == "__main__":
    main()