#!/usr/bin/env python3

import zipfile, os, re, hashlib, json, subprocess, shutil

def main():

    packs_maps = []
    packs_other  = []
    packs_corrupt = []
    
    path_packages = './resources/packages/'
    path_mapshots = './static/mapshots/'
    extract_mapshots = True

    # for f in entities/*.ent; do cat $f |egrep "(item_|weapon_|player)" |awk '{ print $2"," }' |sort |uniq; done |sort |uniq
    entities_list = [
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
            data['bsp'] = []
            data['entities'] = {}
            bsps = []
            bspnames = {}
            #data['entities'] = dict.fromkeys(entities_list, 0)
 
            try:
                zip = zipfile.ZipFile(path_packages + file)
                filelist = zip.namelist()

                # Get the bsp name(s)
                for member in filelist:
                    if re.search('^maps/.*bsp$', member):
                        bspnames[member] = member.replace('maps/','').replace('.bsp','')
                        bsps.append(member)
                        data['bsp'].append(bspnames[member])

                if len(bsps):

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
                                    if bspname not in data['entities']:
                                        data['entities'][bspname] = {}
                                    if entity not in data['entities'][bspname]:
                                        data['entities'][bspname][entity] = 1
                                    else:
                                        data['entities'][bspname][entity] += 1
                        f.close()
                        os.remove(entities_file)
                        shutil.rmtree('./resources/bsp/' + bspname)

                    packs_maps.append(data)
                else:
                    packs_other.append(file)
            
            except zipfile.BadZipfile:
                print('Corrupt file: ' + file)
                packs_corrupt.append(file)
                pass

    output = {}
    output['data'] = packs_maps

    fo = open('./resources/data/entities.json', 'w')
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
