#!/usr/bin/env python3
# Description: Loops through a directory of map pk3s and outputs JSON with map information
# Author: Tyler "-z-" Mulligan

import zipfile, os, re, hashlib, json

def main():

    maplist = []
    
    path = './packages/'

    for file in os.listdir(path):
        if file.endswith('.pk3'):

            data = {}
            data['pk3'] = file
            data['shasum'] = hash_file(path + file)
            data['bsp'] = False
            data['mapshot'] = False
            data['mapinfo'] = False
            data['waypoints'] = False
            data['map'] = False
            data['radar'] = False
            data['title'] = False
            data['description'] = False
            data['gametypes'] = []
            data['author'] = False

            zip = zipfile.ZipFile(path + file)
            filelist = zip.namelist()

            for member in filelist:
                if re.search('^maps/.*bsp$', member):
                    data['bsp'] = member
                elif re.search('^maps/.*jpg$', member):
                    data['mapshot'] = member
                elif re.search('^maps/.*mapinfo$', member):
                    #data['mapinfo'] = member
                    mapinfofile = member
                    data['mapinfo'] = True
                elif re.search('^maps/.*waypoints$', member):
                    #data['waypoints'] = member
                    data['waypoints'] = True
                elif re.search('^maps/.*map$', member):
                    #data['map'] = member
                    data['map'] = True
                elif re.search('^gfx/.*(radar|mini)\.[a-z]{3,4}$', member):
                    data['radar'] = member

            if data['mapinfo'] != False:
                mapinfo = zip.open(mapinfofile)
                
                for line in mapinfo:
                    line = line.decode("unicode_escape").rstrip()
                    if re.search('^title.*$', line):
                        data['title'] = line.partition(' ')[2]
                    elif re.search('^author.*', line):
                        data['author'] = line.partition(' ')[2]
                    elif re.search('^description.*', line):
                        data['description'] = line.partition(' ')[2]
                    elif re.search('^(type|gametype).*', line):
                        data['gametypes'].append(line.partition(' ')[2].partition(' ')[0])

            maplist.append(data)

    output = {}
    output['data'] = maplist

    # for debugging
    print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

    fo = open('data/maps.json', 'w')
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
