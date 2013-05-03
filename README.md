Given an existing tilemill project and a point, this will generate a simple locator map with that point in the center of your tileset.

Example usage:

```bash
python export.py quiet-la lat.png -118.245254 34.052632 0.5 --width=600 
```
Output:

![LA Times](https://github.com/datadesk/tilemill-staticmaps/blob/master/samples/lat.png?raw=true)

Currently there's no way to change the marker's look besides jumping into project-name_staticmaps/staticmap-dynamic.mss and changing the styles there.

