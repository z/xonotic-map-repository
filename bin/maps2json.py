#!/usr/bin/env python3
# Description: Xonotic Map Repository tools help create and manage a map repository.
# Author: Tyler "-z-" Mulligan
# Contact: z@xnz.me

import argparse
import json
from datetime import timedelta
from xmr.packages import *
from xmr.config import config


def main():

    package_distribution = {
        'packs_entities_fail': [],
        'packs_corrupt': [],
        'packs_other': [],
        'packs_maps': [],
    }

    start_time = time.monotonic()

    entities_list = entities_mapping.keys()
    gametype_list = gametype_mapping.keys()

    errors = False

    args = parse_args()

    if args.all:

        # Process all the files
        for file in sorted(os.listdir(config['output_paths']['packages'])):
            if file.endswith('.pk3'):
                status = process_pk3(file, config['output_paths']['packages'], entities_list, gametype_list, package_distribution)
                if status['errors']:
                    errors = True

        # Write error.log
        if errors:
            log_package_errors(package_distribution)

        output = {}
        output['data'] = package_distribution['packs_maps']

        write_to_json(output, config['output_paths']['data'])

    if args.add:

        file = args.add

        if file.endswith('.pk3') and os.path.isfile(config['output_paths']['packages'] + file):
            status = process_pk3(file, config['output_paths']['packages'], entities_list, gametype_list, package_distribution)
            if status['errors']:
                errors = True

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
    print('Operation took: ' + str(timedelta(seconds=end_time - start_time)))


def parse_args():

    parser = argparse.ArgumentParser(description='Xonotic Map Repository tools help create and manage a map repository.')

    parser.add_argument('--add', '-a', nargs='?', type=str, help='Add a package to the repositories JSON')
    parser.add_argument('--all', '-A', action='store_true',
                        help='Add all maps to the repositories JSON. (overwrites existing maps.json)')

    return parser.parse_args()


if __name__ == "__main__":
    main()
