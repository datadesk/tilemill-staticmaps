#! /usr/bin/python

import os
import subprocess
import argparse
from configure import get_bounding_box

tilemill = os.environ.get("TILEMILL", None)
if not tilemill:
    print "You must define $TILEMILL first"
    exit()

parser = argparse.ArgumentParser(description="Render out some static maps")
parser.add_argument('project_name', type=str, help="The tilemill project name to render from.")
parser.add_argument('file_name', type=str, help="The file location to save to.")
parser.add_argument('point', type=float, nargs=2, help="a space-seperated  point in the form lon lat ex -118.48857 34.023925")
parser.add_argument('dist_mi', type=float, help="A distance in miles to the side of the bounding box, ex 0.5 for a half mile on each side")
parser.add_argument('--zoom', type=int, default=14, help="The zoom level.")
parser.add_argument('--width', type=int, default=400, help="width of the resulting image in pixels.")
parser.add_argument('--height', type=int, default=400, help="height of the resulting image in pixels.")
parser.add_argument('--format', type=str, default="png", help="The resulting file format. Defaults to png.")

args = parser.parse_args()

tilemill=os.path.join(tilemill, "index.js")

home = os.environ.get('HOME')
default = os.path.join(home, 'Documents', 'MapBox')
project_dir = os.path.join(os.environ.get('TILEMILL_PROJECTS', default), 'project')

project_name = args.project_name
if not "_staticmaps" in args.project_name:
    project_name = project_name + "_staticmaps"

if not os.path.exists(os.path.join(project_dir, project_name)):
    subprocess.call(["./clone_project.sh",  args.project_name])

subprocess.call(["./configure.py", project_name, ",".join(map(str,args.point))])

bbox = get_bounding_box(args.point[0], args.point[1], args.dist_mi)
subprocess.call([tilemill, "export", project_name, args.file_name, "--format=%s" % args.format, "--bbox=%s" % ",".join(map(str,bbox)), "--minzoom=%s" % args.zoom, "--maxzoom=%s" % args.zoom, "--width=%s" % args.width, "--height=%s" % args.height])

