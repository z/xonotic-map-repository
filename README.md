# xonotic-map-repository
An effort to improve map packages and the services around them.

![xonotic-map-repository](resources/images/xonotic-map-repository.png)

Companion project, [xonotic-map-manager](https://github.com/z/xonotic-map-manager), is a command-line interface package manager.

### Why?

There are approximately 12,500 map packages currently in distribution amongst Xonotic servers. Some of these are ported from other games that support the bsp format, (Nexuiz, quake3, WoP, etc). Many of these packages could use some love, they are missing information that could help them integrate better with Xonotic, and help players identify them.

### Requirements

These files are written in Python 3 using the standard libraries, with the exception of "entities_map.py".

See the requirements below.

```
[default]
# requires imagemagick
extract_mapshots = True

# requires matplotlib and imagemagick
extract_radars = False

# Requires nothing
parse_entities = True
```

### What do these files do?

**maps2json.py** - identifies map packages within a directory of pk3s, extrapolates data about the package and puts it into a JSON document.

**chart_json.py** - consolidates data into another JSON document that's readable by a reusable chart library, c3.

**index.html** - the web front-end for the generated JSON documents.

### TL;DR

1. Copy a whole bunch of pk3s into the `./web/resources/packages` folder
2. run `./bin/maps2json.py -A`
3. run `./bin/chart_json.py`
4. cd `web` && run `python -m SimpleHTTPServer`
5. Goto `http://127.0.0.1:8000`
6. (optional) check `error.log` for any pk3s that were found without bsps and corrupt packs


### Developers

The JSON structure for a map package is as follows:

```json
{
  "data": [
    {
      "filesize": 7856907,
      "date": 1453749340,
      "bsp": {
        "vapor_alpha_2": {
          "title": "Vapor",
          "license": true,
          "map": "maps/vapor_alpha_2.map",
          "gametypes": [
            "ctf",
            "dm"
          ],
          "radar": "gfx/vapor_alpha_2_mini.tga",
          "waypoints": "",
          "description": "Such CTF. Many Vehicles. Wow.",
          "mapinfo": "maps/vapor_alpha_2.mapinfo",
          "entities": {
            "info_player_deathmatch": 4,
            "info_player_team1": 11,
            "info_player_team2": 11,
            "item_armor_big": 10,
            "item_armor_large": 4,
            "item_armor_medium": 16,
            "item_armor_small": 124,
            "item_bullets": 10,
            "item_cells": 14,
            "item_flag_team1": 1,
            "item_flag_team2": 1,
            "item_health_large": 6,
            "item_health_medium": 30,
            "item_health_mega": 2,
            "item_health_small": 100,
            "item_invincible": 1,
            "item_rockets": 20,
            "item_strength": 1,
            "weapon_crylink": 4,
            "weapon_devastator": 6,
            "weapon_electro": 2,
            "weapon_grenadelauncher": 6,
            "weapon_hagar": 4,
            "weapon_machinegun": 6,
            "weapon_vortex": 4
          },
          "mapshot": "maps/vapor_alpha_2.jpg",
          "author": "-z-"
        }
      },
      "pk3": "map-vapor_alpha_2.pk3",
      "shasum": "3df0143516f72269f465070373f165c8787964d5"
    }
  ]
}
```

Entities that are currently parsed can be found in `./bin/entities.py`

### Contributing

Find me in #xonotic on irc.quakenet.org, I'm open to any ideas to improve upon this effort.
