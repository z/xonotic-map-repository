#!/usr/bin/env python3
# Description: Xonotic Map Repository tools help create and manage a map repository.
# Author: Tyler "-z-" Mulligan
# Contact: z@xnz.me

import argparse
import json
import time
import os
import datetime
from xmr.packages import Library
from xmr.packages import MapPackage
from xmr.config import config
from xmr.util import ObjectEncoder


def main():

    start_time = time.monotonic()
    errors = False
    args = parse_args()

    library = Library()

    if args.all:

        # Process all the files
        for file in sorted(os.listdir(config['output_paths']['packages'])):
            if file.endswith('.pk3'):
                mypk3 = MapPackage(pk3_file=file)
                pk3, category, errors = mypk3.process_package()

                print(pk3.pk3_file)

                library.add_map_package(pk3=pk3, category=category)

                # if status['errors']:
                #     errors = True

        # Write error.log
        # if errors:
        #     log_package_errors(package_distribution)

        all_maps = json.dumps({'data': library.maps}, cls=ObjectEncoder)

        fo = open(config['output_paths']['data'] + 'maps.json', 'w')
        fo.write(all_maps)
        fo.close()

    if args.add:

        file = args.add

        if file.endswith('.pk3') and os.path.isfile(config['output_paths']['packages'] + file):
            status = MapPackage(pk3_file=file)

            # if status['errors']:
            #     errors = True

        else:
            print('Not found or not pk3.')
            raise SystemExit

        # Write error.log
        if errors:
            log_package_errors(package_distribution)

        maps_json_file = config['output_paths']['data'] + 'data/maps.json'

        if os.path.isfile(maps_json_file):

            f = open(maps_json_file)
            data = f.read()
            maps_json = json.loads(data)['data']
            f.close()

            for new_package in package_distribution['packs_maps']:
                maps_json.append(new_package)

            output = {}
            output['data'] = maps_json

        else:
            output = {}
            output['data'] = package_distribution['packs_maps']

        write_to_json(output, config['output_paths']['data'])

    end_time = time.monotonic()
    #print(packages)
    print('Operation took: ' + str(datetime.timedelta(seconds=end_time - start_time)))


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


def parse_args():

    parser = argparse.ArgumentParser(description='Xonotic Map Repository tools help create and manage a map repository.')

    parser.add_argument('--add', '-a', nargs='?', type=str, help='Add a package to the repositories JSON')
    parser.add_argument('--all', '-A', action='store_true',
                        help='Add all maps to the repositories JSON. (overwrites existing maps.json)')

    return parser.parse_args()


if __name__ == "__main__":
    main()
