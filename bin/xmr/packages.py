import zipfile
import re
import os
import json
import shutil
import subprocess
import collections
from datetime import datetime
from xmr.util import hash_file
from xmr.util import ObjectEncoder
from xmr.entities import entities_mapping
from xmr.gametypes import gametype_mapping
from xmr.config import config
#from wand.image import Image


class Library(object):
    """
    A Library is a collection of MapPackage Objects
    """
    def __init__(self):
        self.maps = []
        self.entities_fail = []
        self.corrupt = []
        self.other = []

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return self.maps

    def to_json(self):
        return json.dumps({'data': self.maps}, cls=ObjectEncoder)

    def add_map_package(self, pk3=None, category=''):
        if category is 'maps':
            self.maps.append(pk3)
        elif category is 'entities_fail':
            self.entities_fail.append(pk3)
        elif category is 'corrupt':
            self.entities_fail.append(pk3)
        else:
            self.other.append(pk3)


class MapPackage(object):
    """
    Map package is a zip file that has meta data and a dictionary of pk3 objects
    """
    def __init__(self, pk3_file='', entities_list=entities_mapping.keys(), gametypes_list=gametype_mapping.keys()):

        path_packages = config['output_paths']['packages']

        data = {
            'pk3_file': pk3_file,
            'shasum': hash_file(path_packages + pk3_file),
            'filesize': os.path.getsize(path_packages + pk3_file),
            'date': os.path.getmtime(path_packages + pk3_file),
            'bsp': {}
        }

        self.pk3_file = pk3_file
        self.path = config['output_paths']['packages']
        self.shasum = data['shasum']
        self._bsp = data['bsp']
        self.date = data['date']
        self.filesize = data['filesize']
        self.entities_list = entities_list
        self.gametypes_list = gametypes_list

    @property
    def bsp(self):
        return self._bsp

    @bsp.setter
    def bsp(self, key, value):
        self._bsp[key] = value

    @bsp.deleter
    def bsp(self, key):
        del self._bsp[key]

    def __repr__(self):
        return 'MapPackage(pk3=%s, shasum=%s, bsp=%s, date=%s, filesize=%s)' % (self.pk3_file, self.shasum, repr(self.bsp), self.date, self.filesize)

    def __json__(self):
        return {
            'pk3': self.pk3_file,
            'shasum': self.shasum,
            'filesize': self.filesize,
            'date': self.date,
            'bsp': self.bsp,
        }

    def to_json(self):
        return json.dumps({'data': self}, cls=ObjectEncoder)

    def process_package(self):

        data = {'bsp': {}}
        category = 'other'
        errors = {}

        path_bsp = config['output_paths']['bsp']
        path_entities = config['output_paths']['entities']
        path_mapshots = config['output_paths']['mapshots']
        path_radars = config['output_paths']['radars']

        # temp variables
        bsps = []
        bsp_names = {}

        try:
            zip = zipfile.ZipFile(self.path + self.pk3_file)
            filelist = zip.namelist()

            package_bsps = {}

            # Get the bsp name(s)
            for member in filelist:
                if re.search('^maps/.*bsp$', member):
                    bsp_info = zip.getinfo(member)
                    bsp_name = member.replace('maps/', '').replace('.bsp', '')
                    bsp_names[member] = bsp_name
                    # this is coming back as a float
                    epoch = int(datetime(*bsp_info.date_time).timestamp())
                    data['date'] = epoch
                    bsps.append(member)

                    temp = {
                        'bsp_name': bsp_name,
                        'bsp_file': member,
                        'mapshot': "",
                        'mapinfo': "",
                        'waypoints': "",
                        'map_file': "",
                        'radar': "",
                        'title': "",
                        'description': "",
                        'author': "",
                        'license': False,
                        'gametypes': []
                    }

                    data['bsp'][bsp_names[member]] = temp.copy()

                    package_bsps[bsp_name] = self.add_bsp(**temp)

            # One or more bsps has been found (it's a map package)
            if len(bsps):

                # If this option is on, attempt to extract enitity info
                if config['parse_entities'] == 'True':

                    for bsp in bsps:
                        bspname = bsp_names[bsp]

                        zip.extract(bsp, path_bsp + bspname)

                        entities = package_bsps[bspname].extract_entities_file()

                        # print(entities)
                        # print(errors)
                        # shutil.rmtree(path_bsp + bspname)

                # Find out which of the important files exist in the package
                for member in filelist:
                    for bsp in data['bsp']:

                        bspname = bsp
                        rbsp = re.escape(bsp)

                        if re.search('^maps/' + rbsp + '\.ent', member):
                            if config['parse_entities'] == 'True':
                                zip.extract(member, path_entities + bspname)

                                entities_file = path_entities + bspname + '/' + member
                                entities_from_ent, entity_errors = package_bsps[bspname].parse_entities_file(entities_file=entities_file)
                                data['bsp'][bspname].update(entities_from_ent)
                                # shutil.rmtree(path_entities + bspname)

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
                                # subprocess.call(['./bin/entities_map.py', bsp])

                        if re.search('^maps/' + rbsp + '\.map$', member):
                            data['bsp'][bspname]['map_file'] = member

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
                                    if gametype in self.gametypes_list:
                                        gametypes.append(gametype_mapping[gametype])

                            data['bsp'][bspname]['gametypes'].extend(gametypes)

                category = 'maps'
                bsp_meta = data['bsp'][bspname]
                self.add_bsp(**bsp_meta)
            else:
                errors = True
                category = 'other'

        except zipfile.BadZipfile:
            errors = True
            category = 'corrupt'
            print('Corrupt file: ' + self.pk3_file)
            pass

        return self, category, errors

    def add_bsp(self, pk3_file='', bsp_name='', bsp_file='', map_file='', mapshot='', radar='', title='', description='', mapinfo='', author='', gametypes=None, entities=None, waypoints='', license=False, entities_list=entities_mapping.keys(), gametypes_list=gametype_mapping.keys()):
        bsp = Bsp(
            pk3_file=pk3_file,
            bsp_name=bsp_name,
            bsp_file=bsp_file,
            map_file=map_file,
            mapshot=mapshot,
            radar=radar,
            title=title,
            description=description,
            mapinfo=mapinfo,
            author=author,
            gametypes=gametypes,
            entities=entities,
            waypoints=waypoints,
            license=license,
            entities_list=entities_list,
            gametypes_list=gametypes_list
        )
        self.bsp.update({bsp_name: bsp})
        return bsp


class Bsp(object):

    def __init__(self, pk3_file='', bsp_name='', bsp_file='', map_file='', mapshot='', radar='', title='', description='', mapinfo='', author='', gametypes=None, entities=None, entities_file='', waypoints='', license=False, entities_list=entities_mapping.keys(), gametypes_list=gametype_mapping.keys()):
        self.pk3_file = pk3_file
        self.bsp_name = bsp_name
        self.bsp_file = bsp_file
        self.map_file = map_file
        self.mapshot = mapshot
        self.radar = radar
        self.title = title
        self.description = description
        self.mapinfo = mapinfo
        self.author = author
        self.gametypes = gametypes
        self.entities = entities
        self.entities_file = entities_file
        self.waypoints = waypoints
        self.license = license
        self.entities_list = entities_list
        self.gametypes_list = gametypes_list

    # def __repr__(self):
    #     return str(vars(self))

    def __repr__(self):
        return 'Bsp(pk3_file=%s, bsp_name=%s, bsp_file=%s, map_file=%s, mapshot=%s, radar=%s, title=%s, description=%s, mapinfo=%s, author=%s, gametypes=%s, entities=%s, waypoints=%s, license=%s)' % (
        self.pk3_file, self.bsp_name, self.bsp_file, self.map_file, self.mapshot, self.radar, self.title, self.description, self.mapinfo, self.author, self.gametypes, self.entities, self.waypoints, self.license)

    def __json__(self):
        return {
            'map': self.map_file,
            'mapshot': self.mapshot,
            'radar': self.radar,
            'title': self.title,
            'description': self.description,
            'mapinfo': self.mapinfo,
            'author': self.author,
            'gametypes': self.gametypes,
            'entities': self.entities,
            'waypoints': self.waypoints,
            'license': self.license,
        }

    def to_json(self):
        return json.dumps({'data': self}, cls=ObjectEncoder)

    def extract_entities_file(self):

        path_entities = config['output_paths']['entities']
        path_bsp = config['output_paths']['bsp'] + self.bsp_name + '/'
        bsp_entities_file = path_entities + self.bsp_name + '.ent'

        try:
            os.makedirs(path_entities)
        except OSError:
            pass

        with open(bsp_entities_file, 'w') as f:
            subprocess.call(["./bin/bsp2ent", path_bsp + self.bsp_file], stdin=subprocess.PIPE, stdout=f)

    def parse_entities_file(self, entities_file=''):

        bsp = {'entities': {}}
        errors = {}

        if not entities_file:
            path_entities = config['output_paths']['entities']
            bsp_entities_file = path_entities + self.bsp_name + '.ent'

            if not os.path.exists(bsp_entities_file):
                self.extract_entities_file()
                self.parse_entities_file()
        else:
            bsp_entities_file = entities_file

        try:
            f = open(bsp_entities_file)
            for line in iter(f):
                for entity in self.entities_list:
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
            #os.remove(bsp_entities_file)

        except UnicodeDecodeError:
            errors = True
            #category = 'entities_fail'
            bsp['entities'] = {}
            print("Failed to parse entities file for: " + self.bsp_file)

        self.entities = bsp['entities']

        return bsp, errors
