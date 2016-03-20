#!/usr/bin/env python3
# Description: Loops through a directory of map pk3s and outputs JSON with map information
# Author: Tyler "-z-" Mulligan

import zipfile
import os
import re
import hashlib
import json
import subprocess
import shutil
import collections
import time
from datetime import datetime
from datetime import timedelta
from entities import entities_dict

# Config
extract_mapshots = True
parse_entities = True

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resources_dir = root_dir + '/resources/'
path_packages = resources_dir + 'packages/'
path_mapshots = resources_dir + 'mapshots/'

# Temp vars
packs_entities_fail = []
packs_corrupt = []
packs_other  = []
packs_maps = []

entities_list = entities_dict.keys()

errors = False


def main():

    start_time = time.monotonic()

    # Process all the files
    for file in sorted(os.listdir(path_packages)):
        if file.endswith('.pk3'):
            process_pk3(file)

    # Write error.log
    if errors:
        dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        fo = open('error.log', 'a')

        if len(packs_other) != 0:
            e_no_map = 'One or more archives did not contain a map'
            print('\n' + e_no_map)

            fo.write('\n' + dt + ' - ' + e_no_map + ':\n')
            fo.write('\n'.join(packs_other) + '\n')

        if len(packs_corrupt) != 0:
            e_corrupt = 'One or more archives were corrupt'
            print('\n' + e_corrupt)

            fo.write('\n' + dt + ' - ' + e_corrupt + ':\n')
            fo.write('\n'.join(packs_corrupt) + '\n')

        if len(packs_entities_fail) != 0:
            e_no_map = 'One or more entities files failed to parse'
            print('\n' + e_no_map)

            fo.write('\n' + dt + ' - ' + e_no_map + ':\n')
            fo.write('\n'.join(packs_entities_fail) + '\n')

        fo.close()

    output = {}
    output['data'] = packs_maps

    # for debugging
    print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

    fo = open(resources_dir + 'data/maps.json', 'w')
    fo.write(json.dumps(output))
    fo.close()

    end_time = time.monotonic()
    print(timedelta(seconds=end_time - start_time))


def process_pk3(file):

    print('Processing ' + file)

    data = {}
    data['pk3'] = file
    data['shasum'] = hash_file(path_packages + file)
    data['filesize'] = os.path.getsize(path_packages + file)
    data['date'] = os.path.getmtime(path_packages + file)
    data['bsp'] = {}
    data['mapshot'] = []
    data['mapinfo'] = []
    data['waypoints'] = []
    data['map'] = []
    data['radar'] = []
    data['title'] = []
    data['description'] = []
    data['gametypes'] = []
    data['author'] = []
    data['license'] = []

    # temp variables
    bsps = []
    bspnames = {}

    try:
        zip = zipfile.ZipFile(path_packages + file)
        filelist = zip.namelist()

        # Get the bsp name(s)
        for member in filelist:
            if re.search('^maps/.*bsp$', member):
                bsp_info = zip.getinfo(member)
                bspnames[member] = member.replace('maps/', '').replace('.bsp', '')
                # this is coming back as a float
                epoch = int(datetime(*bsp_info.date_time).timestamp())
                data['date'] = epoch
                bsps.append(member)
                data['bsp'][bspnames[member]] = {}

        # One or more bsps has been found (it's a map package)
        if len(bsps):

            # If this option is on, attempt to extract enitity info
            if parse_entities:

                for bsp in bsps:

                    bspname = bspnames[bsp]

                    zip.extract(bsp, resources_dir + 'bsp/' + bspname)

                    bsp_entities_file = resources_dir + 'entities/' + bspname + '.ent'

                    with open(bsp_entities_file, 'w') as f:
                        subprocess.call(["./bin/bsp2ent", resources_dir + 'bsp/' + bspname + "/" + bsp], stdin=subprocess.PIPE, stdout=f)

                    data['bsp'][bspname] = parse_entities_file(data['bsp'][bspname], data['pk3'], bsp_entities_file)

                    shutil.rmtree(resources_dir + 'bsp/' + bspname)

            # Find out which of the important files exist in the package
            for member in filelist:
                for bsp in data['bsp']:

                    rbsp = re.escape(bsp)

                    if re.search('^maps/' + rbsp + '\.(jpg|tga|png)$', member):
                        data['mapshot'].append(member)
                        if extract_mapshots:
                            zip.extract(member, path_mapshots)

                    if re.search('^maps/' + rbsp + '\.mapinfo$', member):
                        data['mapinfo'].append(member)

                    if re.search('^maps/' + rbsp + '\.waypoints$', member):
                        data['waypoints'].append(member)

                    if re.search('^maps/' + rbsp + '\.map$', member):
                        data['map'].append(member)

                    if re.search('^gfx/' + rbsp + '_(radar|mini)\.(jpg|tga|png)$', member):
                        data['radar'].append(member)

                    if re.search('^maps/' + rbsp + '\.ent', member):
                        if parse_entities:
                            zip.extract(member, resources_dir + 'entities/' + bspname)

                            entities_file = resources_dir + 'entities/' + bspname + '/' + member
                            entities_from_ent = parse_entities_file(data['bsp'][bspname], data['pk3'], entities_file)
                            data['bsp'][bspname].update(entities_from_ent)
                            shutil.rmtree(resources_dir + 'entities/' + bspname)

                if re.search('^maps/(LICENSE|COPYING|gpl.txt)$', member):
                    data['license'] = True

            # If the mapinfo file exists, try and parse it
            if len(data['mapinfo']):
                for mapinfofile in data['mapinfo']:

                    mapinfo = zip.open(mapinfofile)
                    gametypes = []

                    for line in mapinfo:
                        line = line.decode('unicode_escape').rstrip()

                        if re.search('^title.*$', line):
                            data['title'].append(line.partition(' ')[2])

                        elif re.search('^author.*', line):
                            data['author'].append(line.partition(' ')[2])

                        elif re.search('^description.*', line):
                            data['description'].append(line.partition(' ')[2])

                        elif re.search('^(type|gametype).*', line):
                            gametypes.append(line.partition(' ')[2].partition(' ')[0])

                    data['gametypes'].append(gametypes)

            packs_maps.append(data)

        else:
            errors = True
            packs_other.append(file)

    except zipfile.BadZipfile:
        errors = True
        print('Corrupt file: ' + file)
        packs_corrupt.append(file)
        pass


def hash_file(filename):
    """This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename,'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def parse_entities_file(bsp, pk3, entities_file):

    try:
        f = open(entities_file)
        for line in iter(f):
            for entity in entities_list:
                real_entity = entities_dict[entity]
                if re.search(entity, line):
                    if 'entities' not in bsp:
                        bsp['entities'] = {}
                    if real_entity not in bsp['entities']:
                        bsp['entities'][real_entity] = 1
                    else:
                        bsp['entities'][real_entity] += 1

        if 'entities' in bsp:
            all_bsp_entities = bsp['entities']
            if len(all_bsp_entities):
                sorted_entities = collections.OrderedDict(sorted(all_bsp_entities.items()))
                bsp['entities'] = sorted_entities

        f.close()
        os.remove(entities_file)

    except UnicodeDecodeError:
        errors = True
        bsp['entities'] = {}
        packs_entities_fail.append(entities_file)
        print("Failed to parse entities file for: " + pk3)

    return bsp

if __name__ == "__main__":
    main()
