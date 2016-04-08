#!/usr/bin/env python3
# Description: Loops through a directory of map pk3s and outputs JSON with map information
# Author: Tyler "-z-" Mulligan

import json
from datetime import timedelta
from xmr.packages import *


def main():

    # Config
    config = read_config('config/config.ini')

    package_distribution = {
        'packs_entities_fail': [],
        'packs_corrupt': [],
        'packs_other': [],
        'packs_maps': [],
    }

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    resources_dir = root_dir + '/resources/'
    path_packages = resources_dir + 'packages/'

    start_time = time.monotonic()

    entities_list = entities_mapping.keys()
    gametype_list = gametype_mapping.keys()

    errors = False

    # Process all the files
    for file in sorted(os.listdir(path_packages)):
        if file.endswith('.pk3'):
            status = process_pk3(file, path_packages, resources_dir, entities_list, gametype_list, config, package_distribution)
            if status['errors']:
                errors = True

    # Write error.log
    if errors:
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

    output = {}
    output['data'] = package_distribution['packs_maps']

    # for debugging
    #print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

    fo = open(resources_dir + 'data/maps.json', 'w')
    fo.write(json.dumps(output))
    fo.close()

    end_time = time.monotonic()
    print(timedelta(seconds=end_time - start_time))


if __name__ == "__main__":
    main()
