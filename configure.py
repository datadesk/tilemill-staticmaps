#! /usr/bin/python

# if you have > 2GB mem, turn this on for slightly faster rendering
feat_caching = True

import os
import math
import json
import sys
from os.path import join

home = os.environ.get('HOME')
default = os.path.join(home, 'Documents', 'MapBox')
project_dir = os.path.join(os.environ.get('TILEMILL_PROJECTS', default), 'project')
tmp_location = "/tmp/staticmap_geojson.json"

def get_bounding_box(longitude_in_degrees, latitude_in_degrees, half_side_in_miles):
    """
    Given lon/lat, return a bbox ready for tilemill.

    Taken from:
    http://stackoverflow.com/questions/1648917/given-a-latitude-and-longitude-and-distance-i-want-to-find-a-bounding-box
    """
    half_side_in_km = half_side_in_miles * 1.609344
    lat = math.radians(latitude_in_degrees)
    lon = math.radians(longitude_in_degrees)

    radius  = 6371
    # Radius of the parallel at given latitude
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - half_side_in_km/radius
    lat_max = lat + half_side_in_km/radius
    lon_min = lon - half_side_in_km/parallel_radius
    lon_max = lon + half_side_in_km/parallel_radius
    rad2deg = math.degrees

    return (
        rad2deg(lon_min),
        rad2deg(lat_min),
        rad2deg(lon_max),
        rad2deg(lat_max),
    )


def prep_mml_layer(lon, lat):
    """
    Takes a lat/lon and writes it to a tmp geojson template.
    """
    geojson_tmpl = """{"type": "Point", "coordinates": [%s,%s]}"""
    

    with open(tmp_location, "w") as f:
        f.write(geojson_tmpl % (lon, lat))
    f.closed
    
    return {
        "geometry": "point",
        "extent": get_bounding_box(lon, lat, 0.5),
        "class": "",
        "Datasource": {
            "file": tmp_location
            },
        "srs": "",
        "srs-name": "autodetect",
        "advanced": {},
        "id": "staticmap-dynamic",
        "name": "staticmap-dynamic"
    }



def doit(project_mml, lon, lat):
    with open(project_mml + ".template", 'r') as f:
      newf = json.loads(f.read())
    f.closed

    with open(project_mml, 'w') as f:
      for layer in newf["Layer"]:
        layer["properties"] = {}
        if feat_caching:
            layer["properties"]["cache-features"] = "true"
      #Drop the new single-point MML in.
      newf["Layer"].append(prep_mml_layer(lon, lat))
      # Link our default point stylesheet
      newf["Stylesheet"].append("staticmap-dynamic.mss")
      f.write(json.dumps(newf, sort_keys=True, indent=2))
    f.closed

if __name__ == "__main__":
    project, point = sys.argv[1:]
    if not '_staticmaps' in project:
       project = project + '_staticmaps'
    lon, lat = map(float, point.split(','))
    target_mml = os.path.join(project_dir, project, 'project.mml')
    doit(target_mml, lon, lat)
