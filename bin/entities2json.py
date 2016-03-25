#!/usr/bin/env python3
# Description: Attempt to convert the entities to valid JSON
# Author: Tyler "-z-" Mulligan

import json
import re


def replace_last(s, old, new):
    return s[::-1].replace(old[::-1], new[::-1], 1)[::-1]


def parse_entity_file(entities_file):

    f = open(entities_file, 'r')
    file_data = f.read()
    f.close()

    # Turn it into JSON
    file_data = re.sub(r'(".*") (".*")', r'\1: \2,', file_data)
    file_data = re.sub(r'(".*": ".*"),\n}', r'\1\n},', file_data)
    file_data = replace_last(file_data, '},', '}')

    entities = json.loads("[" + file_data + "]")

    return entities


def entities_to_json(entities, out_file):
    f = open(out_file, 'w')
    f.write(json.dumps(entities))
    f.close()
