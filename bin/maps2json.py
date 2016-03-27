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
#from wand.image import Image
from datetime import datetime
from datetime import timedelta
from xmr.util import *
from xmr.entities import entities_mapping
from xmr.gametypes import gametype_mapping

# Config
config = read_config('config/config.ini')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resources_dir = root_dir + '/resources/'
path_packages = resources_dir + 'packages/'
path_mapshots = resources_dir + 'mapshots/'
path_radars = resources_dir + 'radars/'

# Temp vars
packs_entities_fail = []
packs_corrupt = []
packs_other = []
packs_maps = []

entities_list = entities_mapping.keys()
gametype_list = gametype_mapping.keys()

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
    #print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

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

                temp = {}
                temp['mapshot'] = ""
                temp['mapinfo'] = ""
                temp['waypoints'] = ""
                temp['map'] = ""
                temp['radar'] = ""
                temp['title'] = ""
                temp['description'] = ""
                temp['author'] = ""
                temp['license'] = False
                temp['gametypes'] = []

                data['bsp'][bspnames[member]] = temp.copy()

        # One or more bsps has been found (it's a map package)
        if len(bsps):

            # If this option is on, attempt to extract enitity info
            if config['parse_entities'] == 'True':

                for bsp in bsps:

                    bspname = bspnames[bsp]

                    zip.extract(bsp, resources_dir + 'bsp/' + bspname)

                    bsp_entities_file = resources_dir + 'entities/' + bspname + '.ent'

                    with open(bsp_entities_file, 'w') as f:
                        subprocess.call(["./bin/bsp2ent", resources_dir + 'bsp/' + bspname + "/" + bsp], stdin=subprocess.PIPE, stdout=f)

                    data['bsp'][bspname] = parse_entities_file(data['bsp'][bspname], data['pk3'], bsp_entities_file)

#                    shutil.rmtree(resources_dir + 'bsp/' + bspname)

            # Find out which of the important files exist in the package
            for member in filelist:
                for bsp in data['bsp']:

                    bspname = bsp
                    rbsp = re.escape(bsp)

                    if re.search('^maps/' + rbsp + '\.ent', member):
                        if config['parse_entities'] == 'True':
                            zip.extract(member, resources_dir + 'entities/' + bspname)

                            entities_file = resources_dir + 'entities/' + bspname + '/' + member
                            entities_from_ent = parse_entities_file(data['bsp'][bspname], data['pk3'], entities_file)
                            data['bsp'][bspname].update(entities_from_ent)
#                            shutil.rmtree(resources_dir + 'entities/' + bspname)

                    if re.search('^maps/' + rbsp + '\.(jpg|tga|png)$', member):
                        data['bsp'][bspname]['mapshot'] = member
                        if config['extract_mapshots'] == 'True':
                            zip.extract(member, path_mapshots)
                            mapshot_image = path_mapshots + member
                            if member.endswith('.tga'):
                                subprocess.call(['convert', mapshot_image, path_mapshots + 'maps/' + bsp + '.jpg'])

                    if re.search('^gfx/' + rbsp + '_(radar|mini)\.(jpg|tga|png)$', member):
                        data['bsp'][bspname]['radar'] = member
                        if config['extract_radars'] == 'True':
                            zip.extract(member, path_radars)
                            radar_image = path_radars + member
                            subprocess.call(['convert', radar_image, '-depth', '8', '-trim', 'PNG24:' + path_radars + 'gfx/' + bsp + '_mini.png'])
                            
                            subprocess.call(['./bin/entities_map.py', bsp])

#                            image = Image(filename=(radar_image))
#                            with image.convert('PNG24') as converted:
#                                converted.transform_colorspace('rgb')
#                                converted.depth = 8
#                                converted.trim()
#                                converted.save(filename=path_radars + 'gfx/' + bsp + '_mini.png')

                    if re.search('^maps/' + rbsp + '\.map$', member):
                        data['bsp'][bspname]['map'] = member

                    if re.search('^maps/' + rbsp + '\.waypoints$', member):
                        data['bsp'][bspname]['waypoints'] = member

                    if re.search('(LICENSE|COPYING|gpl.txt)', member):
                        data['bsp'][bspname]['license'] = True

                    if re.search('^maps/' + rbsp + '\.mapinfo$', member):
                        data['bsp'][bspname]['mapinfo'] = member

                        mapinfo = zip.open(data['bsp'][bspname]['mapinfo'])
                        gametypes = []

                        for line in mapinfo:
                            line = line.decode('unicode_escape').rstrip()

                            if re.search('^title.*$', line):
                                data['bsp'][bspname]['title'] = line.partition(' ')[2]

                            elif re.search('^author.*', line):
                                data['bsp'][bspname]['author'] = line.partition(' ')[2]

                            elif re.search('^description.*', line):
                                data['bsp'][bspname]['description'] = line.partition(' ')[2]

                            elif re.search('^(type|gametype).*', line):
                                gametype = line.partition(' ')[2].partition(' ')[0]
                                if gametype in gametype_list:
                                    gametypes.append(gametype_mapping[gametype])

                        data['bsp'][bspname]['gametypes'].extend(gametypes)
                    
            packs_maps.append(data)

        else:
            errors = True
            packs_other.append(file)

    except zipfile.BadZipfile:
        errors = True
        print('Corrupt file: ' + file)
        packs_corrupt.append(file)
        pass


def parse_entities_file(bsp, pk3, entities_file):

    try:
        f = open(entities_file)
        for line in iter(f):
            for entity in entities_list:
                real_entity = entities_mapping[entity]
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
        # os.remove(entities_file)

    except UnicodeDecodeError:
        errors = True
        bsp['entities'] = {}
        packs_entities_fail.append(entities_file)
        print("Failed to parse entities file for: " + pk3)

    return bsp


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


if __name__ == "__main__":
    main()
