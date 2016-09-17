import zipfile
import re
import json
import shutil
import subprocess
import collections
from datetime import datetime
from xmr.util import *
from xmr.entities import entities_mapping
from xmr.gametypes import gametype_mapping
#from wand.image import Image
# mkdir {bsp,data,entities,images,mapshots}


def process_pk3(file, path_packages, resources_dir, entities_list, gametype_list, config, package_distribution):

    print('Processing ' + file)

    path_mapshots = resources_dir + 'mapshots/'
    path_radars = resources_dir + 'radars/'
    path_entities = resources_dir + 'entities/'
    path_bsp = resources_dir + 'bsp/'
    path_data = resources_dir + 'data/'

    os.makedirs(path_mapshots, exist_ok=True)
    os.makedirs(path_radars, exist_ok=True)
    os.makedirs(path_entities, exist_ok=True)
    os.makedirs(path_bsp, exist_ok=True)
    os.makedirs(path_data, exist_ok=True)

    data = {}
    data['pk3'] = file
    data['shasum'] = hash_file(path_packages + file)
    data['filesize'] = os.path.getsize(path_packages + file)
    data['date'] = os.path.getmtime(path_packages + file)
    data['bsp'] = {}

    errors = False

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

                    zip.extract(bsp, path_bsp + bspname)

                    bsp_entities_file = path_entities + bspname + '.ent'

                    with open(bsp_entities_file, 'w') as f:
                        subprocess.call(["./bin/bsp2ent", path_bsp + bspname + "/" + bsp], stdin=subprocess.PIPE, stdout=f)

                    data['bsp'][bspname], entity_errors = parse_entities_file(data['bsp'][bspname], data['pk3'], bsp_entities_file, entities_list, package_distribution)

                    shutil.rmtree(path_bsp + bspname)

            # Find out which of the important files exist in the package
            for member in filelist:
                for bsp in data['bsp']:

                    bspname = bsp
                    rbsp = re.escape(bsp)

                    if re.search('^maps/' + rbsp + '\.ent', member):
                        if config['parse_entities'] == 'True':
                            zip.extract(member, path_entities + bspname)

                            entities_file = path_entities + bspname + '/' + member
                            entities_from_ent, entity_errors = parse_entities_file(data['bsp'][bspname], data['pk3'], entities_file, entities_list, package_distribution)
                            data['bsp'][bspname].update(entities_from_ent)
                            shutil.rmtree(path_entities + bspname)

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

                           # The Pythonic way isn't working.
                           # image = Image(filename=(radar_image))
                           # with image.convert('PNG24') as converted:
                           #     converted.transform_colorspace('rgb')
                           #     converted.depth = 8
                           #     converted.trim()
                           #     converted.save(filename=path_radars + 'gfx/' + bsp + '_mini.png')

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

            package_distribution['packs_maps'].append(data)

        else:
            errors = True
            package_distribution['packs_other'].append(file)

    except zipfile.BadZipfile:
        errors = True
        print('Corrupt file: ' + file)
        package_distribution['packs_corrupt'].append(file)
        pass

    status = {}
    status['errors'] = errors

    return status


def parse_entities_file(bsp, pk3, entities_file, entities_list, package_distribution):

    errors = False

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
        os.remove(entities_file)

    except UnicodeDecodeError:
        errors = True
        bsp['entities'] = {}
        package_distribution['packs_entities_fail'].append(entities_file)
        print("Failed to parse entities file for: " + pk3)

    return bsp, errors


def log_package_errors(package_distribution):
    dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    fo = open('error.log', 'a')

    if len(package_distribution['packs_other']) != 0:
        e_no_map = 'One or more archives did not contain a map'
        print('\n' + e_no_map)

        fo.write('\n' + dt + ' - ' + e_no_map + ':\n')
        fo.write('\n'.join(package_distribution['packs_other']) + '\n')

    if len(package_distribution['packs_corrupt']) != 0:
        e_corrupt = 'One or more archives were corrupt'
        print('\n' + e_corrupt)

        fo.write('\n' + dt + ' - ' + e_corrupt + ':\n')
        fo.write('\n'.join(package_distribution['packs_corrupt']) + '\n')

    if len(package_distribution['packs_entities_fail']) != 0:
        e_no_map = 'One or more entities files failed to parse'
        print('\n' + e_no_map)

        fo.write('\n' + dt + ' - ' + e_no_map + ':\n')
        fo.write('\n'.join(package_distribution['packs_entities_fail']) + '\n')

    fo.close()


def write_to_json(output, resources_dir):
    # for debugging
    # print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

    path_data = resources_dir + 'data/'

    fo = open(path_data + 'maps.json', 'w')
    fo.write(json.dumps(output))
    fo.close()
