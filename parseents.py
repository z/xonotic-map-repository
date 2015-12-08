#!/usr/bin/env python3

import zipfile, os, re, subprocess, json

def main():

    packs_maps = []
    packs_other  = []
    packs_corrupt = []
    
    path_packages = './packages/'
    path_mapshots = './mapshots'
    extract_mapshots = True

    for file in sorted(os.listdir(path_packages)):
        if file.endswith('.pk3'):

            print('Processing ' + file)

            data = {}
            data['pk3'] = file
            data['bsp'] = []
 
            try:
                zip = zipfile.ZipFile(path_packages + file)
                filelist = zip.namelist()

                # Get the bsp name(s)
                for member in filelist:
                    if re.search('^maps/.*bsp$', member):
                        data['bsp'].append(member)
                        bspname = member.replace('maps/','').replace('.bsp','')

                if len(data['bsp']):

                    zip.extract(data['bsp'][0], './bsp/' + bspname)

                    with open('./entities/' + bspname + '.ent', 'w') as f:
                        subprocess.call(["./bsp2ent", 'bsp/' + bspname + "/" + data['bsp'][0]], stdin=subprocess.PIPE, stdout=f)

                if len(data['bsp']):
                    packs_maps.append(data)
                else:
                    packs_other.append(file)
            
            except zipfile.BadZipfile:
                print('Corrupt file: ' + file)
                packs_corrupt.append(file)
                pass

#    fo = open('data/entities.json', 'w')
#    fo.write(json.dumps(output))
#    fo.close()

if __name__ == "__main__":
    main()
