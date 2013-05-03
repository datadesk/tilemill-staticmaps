Given an existing tilemill project and a point, this will generate a simple locator map with that point in the center of your tileset.

Requires you export a $TILLEMILL variable to point to your install. Tries to guess your TileMill projects location, but export TILEMILL_PROJECTS if it can't seem to find it.

Example usage:

```bash
$ export TILEMILL=/usr/share/tilemill
$ python export.py quiet-la lat.png -118.245254 34.052632 0.5 --width=600 
```
Output:

![LA Times](https://github.com/datadesk/tilemill-staticmaps/blob/master/samples/lat.png?raw=true)

Currently there's no way to change the marker's look besides jumping into project-name_staticmaps/staticmap-dynamic.mss and changing the styles there.

I've only tested this on Ubuntu 12.04.
