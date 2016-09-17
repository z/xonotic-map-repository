import os
import configparser

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = root_dir + '/config/config.ini'
resources_dir = root_dir + '/web/resources/'

if not os.path.isfile(config_file):
    raise SystemExit(config_file + ' not found, please create one.')

config = configparser.ConfigParser()
config.read(config_file)

conf = config['default']

config = {
    'extract_mapshots': conf['extract_mapshots'],
    'extract_radars': conf['extract_radars'],
    'parse_entities': conf['parse_entities'],
    'resources_dir': root_dir + conf['resources_dir'],
    'output_paths': {
        'packages': conf['resources_dir'] + 'packages/',
        'mapshots': conf['resources_dir'] + 'mapshots/',
        'radars': conf['resources_dir'] + 'radars/',
        'entities': conf['resources_dir'] + 'entitires/',
        'bsp': conf['resources_dir'] + 'bsp/',
        'data': conf['resources_dir'] + 'data/',
    }
}

os.makedirs(config['output_paths']['mapshots'], exist_ok=True)
os.makedirs(config['output_paths']['radars'], exist_ok=True)
os.makedirs(config['output_paths']['entities'], exist_ok=True)
os.makedirs(config['output_paths']['bsp'], exist_ok=True)
os.makedirs(config['output_paths']['data'], exist_ok=True)
