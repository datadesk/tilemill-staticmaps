Given an existing tilemill project and a point, this will generate a simple locator map with that point in the center of your tileset.

Example usage:

```bash
 ./export.py quiet-la test.png -118.48857 34.023926 0.5 --width=300 --height=300
```
Output:

![SaMo](https://github.com/datadesk/tilemill-staticmaps/blob/master/samples/test.png?raw=true)

Currently there's no way to change the marker's look besides jumping into project-name_staticmaps/staticmap-dynamic.mss and changing the styles there.

