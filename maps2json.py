#!/usr/bin/env python3
# Description: Loops through a directory of map pk3s and outputs JSON with map information
# Author: Tyler "-z-" Mulligan

import zipfile, os, re, hashlib, json, subprocess, shutil
from datetime import datetime
            
def main():

    packs_maps = []
    packs_other  = []
    packs_corrupt = []
    
    path_packages = './resources/packages/'
    path_mapshots = './resources/mapshots/'
    extract_mapshots = True
    parse_entities = True

    # for f in entities/*.ent; do cat $f |egrep "(item_|weapon_|player)" |awk '{ print $2"," }' |sort |uniq; done |sort |uniq
    entities_list = [
        "ammo_bfg",
        "ammo_bullets",
        "ammo_cells",
        "ammo_grenades",
        "ammo_lightning",
        "ammo_nails",
        "ammo_rockets",
        "ammo_shells",
        "ammo_slugs",
        "info_player_deathmatch",
        "info_player_intermission",
        "info_player_start",
        "info_player_team1",
        "info_player_team2",
        "item_ammoregen",
        "item_armor1",
        "item_armor25",
        "item_armor_big",
        "item_armor_body",
        "item_armor_combat",
        "item_armor_large",
        "item_armor_medium",
        "item_armor_shard",
        "item_armor_small",
        "item_botroam",
        "item_buff_arc_team1",
        "item_buff_arc_team2",
        "item_buff_guard_team1",
        "item_buff_guard_team2",
        "item_buff_haste_team1",
        "item_buff_haste_team2",
        "item_buff_medic_team1",
        "item_buff_medic_team2",
        "item_buff_supply_team1",
        "item_buff_supply_team2",
        "item_bullets",
        "item_cells",
        "item_doubler",
        "item_enviro",
        "item_flag_team1",
        "item_flag_team2",
        "item_flight",
        "item_guard",
        "item_haste",
        "item_health",
        "item_health1",
        "item_health100",
        "item_health25",
        "item_health_large",
        "item_health_medium",
        "item_health_medium1",
        "item_health_mega",
        "item_health_small",
        "item_health_small1",
        "item_invincible",
        "item_invis",
        "item_minst_cells",
        "item_quad",
        "item_regen",
        "item_rockets",
        "item_rockets1",
        "item_scout",
        "item_shells",
        "item_strength",
        "team_CTF_blueplayer",
        "team_CTF_redplayer",
        "weapon_arc",
        "weapon_bfg",
        "weapon_campingrifle",
        "weapon_chaingun",
        "weapon_crylink",
        "weapon_electro",
        "weapon_grenadelauncher",
        "weapon_hagar",
        "weapon_hlac",
        "weapon_laser",
        "weapon_lightning",
        "weapon_machinegun",
        "weapon_minstanex",
        "weapon_nailgun",
        "weapon_nex",
        "weapon_plasmagun",
        "weapon_porto",
        "weapon_railgun",
        "weapon_rifle",
        "weapon_rocketlauncher",
        "weapon_seeker",
        "weapon_shotgun",
        "weapon_uzi",
    ]

    for file in sorted(os.listdir(path_packages)):
        if file.endswith('.pk3'):

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
            data['title'] = False
            data['description'] = False
            data['gametypes'] = []
            data['author'] = False
            data['license'] = False

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
                        bspnames[member] = member.replace('maps/','').replace('.bsp','')
                        # this is coming back as a float
                        epoch = int(datetime(*bsp_info.date_time).timestamp())
                        data['date'] = epoch
                        bsps.append(member)
                        data['bsp'][bspnames[member]] = {}

                if len(bsps):

                    if parse_entities:

                        for bsp in bsps:
                            
                            bspname = bspnames[bsp]

                            zip.extract(bsp, './resources/bsp/' + bspname)
                                                               
                            entities_file = './resources/entities/' + bspname + '.ent'
                            with open(entities_file, 'w') as f:
                                subprocess.call(["./bsp2ent", './resources/bsp/' + bspname + "/" + bsp], stdin=subprocess.PIPE, stdout=f)

                            f = open(entities_file)
                            for line in iter(f):
                                for entity in entities_list:
                                    if re.search(entity, line):
                                        if 'entities' not in data['bsp'][bspname]:
                                            data['bsp'][bspname]['entities'] = {}
                                        if entity not in data['bsp'][bspname]['entities']:
                                            data['bsp'][bspname]['entities'][entity] = 1
                                        else:
                                            data['bsp'][bspname]['entities'][entity] += 1

                            f.close()
                            os.remove(entities_file)
                            shutil.rmtree('./resources/bsp/' + bspname)

                    # Find out which of the important files exist in the package
                    for member in filelist:
                        for bsp in data['bsp']:

                            rbsp = re.escape(bsp)

                            if re.search('^maps/' + rbsp + '\.(jpg|tga|png)$', member):
                                data['mapshot'].append(member)
                                if extract_mapshots:
                                    zip.extract(member, path_mapshots)

                            if re.search('^maps/' + rbsp + '\.mapinfo$', member):
                                mapinfofile = member
                                data['mapinfo'].append(member)

                            if re.search('^maps/' + rbsp + '\.waypoints$', member):
                                data['waypoints'].append(member)

                            if re.search('^maps/' + rbsp + '\.map$', member):
                                data['map'].append(member)
    
                            if re.search('^gfx/' + rbsp + '_(radar|mini)\.(jpg|tga|png)$', member):
                                data['radar'].append(member)

                        if re.search('^maps/(LICENSE|COPYING|gpl.txt)$', member):
                            data['license'] = True

                    # If the mapinfo file exists, try and parse it
                    if len(data['mapinfo']):
                        mapinfo = zip.open(mapinfofile)
                        
                        for line in mapinfo:
                            line = line.decode('unicode_escape').rstrip()

                            if re.search('^title.*$', line):
                                data['title'] = line.partition(' ')[2]

                            elif re.search('^author.*', line):
                                data['author'] = line.partition(' ')[2]

                            elif re.search('^description.*', line):
                                data['description'] = line.partition(' ')[2]

                            elif re.search('^(type|gametype).*', line):
                                data['gametypes'].append(line.partition(' ')[2].partition(' ')[0])

                    packs_maps.append(data)
                else:
                    packs_other.append(file)
            
            except zipfile.BadZipfile:
                print('Corrupt file: ' + file)
                packs_corrupt.append(file)
                pass

    if len(packs_other) != 0:
        e_no_map = 'One or more archives did not contain a map'
        print('\n' + e_no_map)

        dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        fo = open('error.log', 'a')
        fo.write('\n' + dt + ' - ' + e_no_map + ':\n')
        fo.write('\n'.join(packs_other) + '\n')
        fo.close()

    if len(packs_corrupt) != 0:
        e_corrupt = 'One or more archives were corrupt'
        print('\n' + e_corrupt)

        dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        fo = open('error.log', 'a')
        fo.write('\n' + dt + ' - ' + e_corrupt + ':\n')
        fo.write('\n'.join(packs_corrupt) + '\n')
        fo.close()

    output = {}
    output['data'] = packs_maps

    # for debugging
    #print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

    fo = open('./resources/data/maps.json', 'w')
    fo.write(json.dumps(output))
    fo.close()


def hash_file(filename):
   """"This function returns the SHA-1 hash
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
