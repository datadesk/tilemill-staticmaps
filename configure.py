#! /usr/bin/python
# For postgres layers mapnik by default will query postgis for the
# extent to know whether to process the layer during rendering
# Increase performance if you are only rendering a particular area by
# specifying a bounding box in the format of "XMIN,YMIN,XMAX,YMAX" in the
# same units as the database (probably spherical mercator meters). The
# whole world is "-20037508.34,-20037508.34,20037508.34,20037508.34".
extent = "-13849828.38,3833234.22,-12705175.77,5162381.7"

# if you have > 2GB mem, turn this on for slightly faster rendering
feat_caching = True

#
# Don't touch this part down here, just run it.
#

import os
import json
import sys
from os.path import join

home = os.environ.get('HOME')
default = os.path.join(home, 'Documents', 'MapBox')
project_dir = os.path.join(os.environ.get('TILEMILL_PROJECTS', default), 'project')
tmp_location = "/tmp/staticmap_geojson.json"

def prep_mml_layer(lat, lon):
    """
    Takes a lat/lon and writes it to a tmp geojson template.
    """
    geojson_tmpl = """{"type": "Point", "coordinates": [%s,%s]}"""
    

    with open(tmp_location, "w") as f:
        f.write(geojson_tmpl % (lat, lon))
    f.closed
    
    return {
        "geometry": "point",
        #"extent": [],
        "id": "staticmap-dynamic",
        "class": "",
        "Datasource": {
            "file": tmp_location
            },
        "srs-name": "autodetect",
        "srs": "",
        "advanced": {},
        "name": "staticmap-dynamic"
    }



def doit(project_mml, lat, lon):
    with open(project_mml + ".template", 'r') as f:
      newf = json.loads(f.read())
    f.closed

    with open(project_mml, 'w') as f:
      for layer in newf["Layer"]:
        layer["properties"] = {}
        if feat_caching:
            layer["properties"]["cache-features"] = "true"
      #Drop the new single-point MML in.
      newf["Layer"].insert(0, prep_mml_layer(lat, lon))
      f.write(json.dumps(newf, sort_keys=True, indent=2))
    f.closed

if __name__ == "__main__":
    project, point = sys.argv[1:]
    if not '_staticmaps' in project:
       project = project + '_staticmaps'
    lat, lon = point.split(',')
    target_mml = os.path.join(project_dir, project, 'project.mml')
    doit(target_mml, lat, lon)
