# xonotic-map-repository
An effort to improve map packages and the services around them.

![xonotic-map-repository](resources/images/xonotic-map-repository.png)

Companion project, [xonotic-map-manager](https://github.com/z/xonotic-map-manager), is a command-line interface package manager.

### Why?

There are approximately 12,500 map packages currently in distribution amongst Xonotic servers. Some of these are ported from other games that support the bsp format, (Nexuiz, quake3, WoP, etc). Many of these packages could use some love, they are missing information that could help them integrate better with Xonotic, and help players identify them.

### What do these files do?

**maps2json.py** - identifies map packages within a directory of pk3s, extrapolates data about the package and puts it into a JSON document.

**chartjson.py** - consolidates data into another JSON document that's readable by a reusable chart library, c3.

**index.html** - the web front-end for the generated JSON documents.

### TL;DR

1. Copy a whole bunch of pk3s into the ./packages folder
2. run `./maps2json.py`
3. run `./chartjson.py`
4. run `python -m SimpleHTTPServer`
5. Goto `http://127.0.0.1:8000`
6. (optional) check `error.log` for any pk3s that were found without bsps and corrupt packs

### Contributing

Find me in #xonotic on irc.quakenet.org, I'm open to any ideas to improve upon this effort.
