#!/usr/bin/env python3

import zipfile, os, re, hashlib, json, subprocess, shutil

def main():

    packs_maps = []
    packs_other  = []
    packs_corrupt = []
    
    path_packages = './resources/packages/'
    path_mapshots = './resources/mapshots/'
    extract_mapshots = True

    entities_dict = {

        # health / armor
        'item_armor_small': 'item_armor_small',
        'item_armor1': 'item_armor_small',
        'item_armor_shard': 'item_armor_small',
        'item_armor_medium': 'item_armor_medium',
        'item_armor_large': 'item_armor_large',
        'item_armor25': 'item_armor_large',
        'item_armor2': 'item_armor_large',
        'item_armor_body': 'item_armor_large',
        'item_armor_big': 'item_armor_big',
        'item_armor_combat': 'item_armor_big',
        'item_armor_mega': 'item_armor_big',
        'item_health_small': 'item_health_small',
        'item_health1': 'item_health_small',
        'item_health_medium': 'item_health_medium',
        'item_health25': 'item_health_medium',
        'item_health_large': 'item_health_large',
        'item_health_mega': 'item_health_mega',
        'item_health100': 'item_health_mega',

        # powerups
        'item_strength': 'item_strength',
        'item_quad': 'item_strength',
        'item_invincible': 'item_invincible',
        'item_enviro': 'item_invincible',

        # flags
        'item_flag_team1': 'item_flag_team1',
        'team_CTF_redflag': 'item_flag_team1',
        'item_flag_team2': 'item_flag_team2',
        'team_CTF_blueflag': 'item_flag_team2',
        'item_flag_team3': 'item_flag_team3',
        'item_flag_team4': 'item_flag_team4',
        'item_flag_neutral': 'item_flag_neutral',

        # ammo
        'item_bullets': 'item_bullets',
        'item_spikes': 'item_bullets',
        'ammo_bullets': 'item_bullets',
        'item_rockets': 'item_rockets',
        'ammo_rockets': 'item_rockets',
        'ammo_grenades': 'item_rockets',
        'ammo_nails': 'item_rockets',
        'ammo_cells': 'item_rockets',
        'item_cells': 'item_cells',
        'ammo_lightning': 'item_cells',
        'ammo_slugs': 'item_cells',
        'ammo_bfg': 'item_cells',
        'item_shells': 'item_shells',
        'ammo_shells': 'item_shells',
        'item_plasma': 'item_plasma',
        'item_minst_cells': 'item_minst_cells',

        # weapons
        'weapon_shotgun': 'weapon_shotgun',
        'weapon_electro': 'weapon_electro',
        'weapon_nailgun': 'weapon_electro',
        'weapon_lightning': 'weapon_electro',
        'weapon_hagar': 'weapon_hagar',
        'weapon_supernailgun': 'weapon_hagar',
        'weapon_plasmagun': 'weapon_hagar',
        'weapon_vortex': 'weapon_vortex',
        'weapon_railgun': 'weapon_vortex',
        'weapon_nex': 'weapon_vortex',
        'weapon_crylink': 'weapon_crylink',
        'weapon_bfg': 'weapon_crylink',
        'weapon_vaporizer': 'weapon_vaporizer',
        'weapon_minstanex': 'weapon_vaporizer',
        'weapon_rifle': 'weapon_rifle',
        'weapon_campingrfile': 'weapon_rifle',
        'weapon_sniperrifle': 'weapon_rifle',
        'weapon_blaster': 'weapon_blaster',
        'weapon_laser': 'weapon_blaster',
        'weapon_devastator': 'weapon_devastator',
        'weapon_rockerlauncher': 'weapon_devastator',
        'weapon_grenadelauncher': 'weapon_grenadelauncher',
        'weapon_mortar': 'weapon_grenadelauncher',
        'weapon_machinegun': 'weapon_machinegun',
        'weapon_uzi': 'weapon_machinegun',
        'weapon_supershotgun': 'weapon_machinegun',
        'weapon_fireball': 'weapon_fireball',
        'weapon_shockwave': 'weapon_shockwave',
        'weapon_seeker': 'weapon_seeker',
        'weapon_arc': 'weapon_arc',
        'weapon_minelayer': 'weapon_minelayer',
        'weapon_hook': 'weapon_hook',

        # player spawns
        'info_player_deathmatch': 'info_player_deathmatch',
        'info_player_team1': 'info_player_team1',
        'team_CTF_redplayer': 'info_player_team1',
        'team_CTF_redspawn': 'info_player_team1',
        'info_player_team2': 'info_player_team2',
        'team_CTF_blueplayer': 'info_player_team2',
        'team_CTF_bluespawn': 'info_player_team2',
        'info_player_team3': 'info_player_team3',
        'info_player_team4': 'info_player_team4',
        'info_player_start': 'info_player_start',
        #'info_player_survivor': 'info_player_survivor',
        #'info_player_race': 'info_player_race',
        #'info_player_attacker': 'info_player_attacker',
        #'info_player_defender': 'info_player_defender'

    }

    entities_list = entities_dict.keys()

    for file in sorted(os.listdir(path_packages)):
        if file.endswith('.pk3'):

            print('Processing ' + file)

            data = {}
            data['pk3'] = file
            data['shasum'] = hash_file(path_packages + file)
            data['bsp'] = {}
            bsps = []
            bspnames = {}
 
            try:
                zip = zipfile.ZipFile(path_packages + file)
                filelist = zip.namelist()

                # Get the bsp name(s)
                for member in filelist:
                    if re.search('^maps/.*bsp$', member):
                        bspnames[member] = member.replace('maps/','').replace('.bsp','')
                        bsps.append(member)
                        data['bsp'][bspnames[member]] = {}

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
                                    print(entity)
                                    real_entity = entities_dict[entity]
                                    if 'entities' not in data['bsp'][bspname]:
                                        data['bsp'][bspname]['entities'] = {}
                                    if real_entity not in data['bsp'][bspname]['entities']:
                                        data['bsp'][bspname]['entities'][real_entity] = 1
                                    else:
                                        data['bsp'][bspname]['entities'][real_entity] += 1
                        f.close()
                        #os.remove(entities_file)
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
