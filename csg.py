#!/usr/bin/env python2

import glob
import math
import os
import argparse
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=str,
                        help="folder with a bunch of .png/gif files")
    parser.add_argument("-o", "--output", type=str, default="out",
                        help="folder to output to")
    parser.add_argument("-g", "--gif", action="store_true",
                        help="use gif files instead of png")
    args = parser.parse_args()

    name = args.folder
    outname = args.output
    ext = 'gif' if args.gif else 'png'

    stuff = glob.glob(name + "/*." + ext)
    if len(stuff) == 0:
        print "No {0}s found in folder {1}".format(ext, name)
        exit(-1)
    width = int(math.ceil(math.sqrt(len(stuff))))
    height = int(math.ceil(len(stuff) / width))

    try:
        os.mkdir(outname)
    except OSError as (e):
        pass

    out = None
    css = open(outname + "/" + name + ".css", "w")
    size = None

    for index, item in enumerate(stuff):
        itemname = item.split(name + "/")[1].split("." + ext)[0]
        img = Image.open(item)
        if index == 0:
            size = img.size
            out = Image.new('RGBA', (width * size[0], (height + 1) * size[1]))
            css.write((".{0} {{"
                       "display: inline-block;"
                       "height: {1}px;"
                       "width: {2}px;"
                       "background: url({0}.{3}) no-repeat 0 0;"
                       "}}\n").format(name, size[0], size[1], ext))
        y = index / width
        x = index % width
        out.paste(img, (x * size[0], y * size[1]))

        css.write((".{0}.{1} {{"
                   "background-position: -{2}px -{3}px"
                   "}}\n").format(name, itemname, x * size[0], y * size[1]))

    out.save(outname + "/" + name + "." + ext, ext.upper(), transparency=0)
    css.close()

    print "Generated {2}/{0}.{1} and {2}/{0}.css".format(name, ext, outname)

if __name__ == "__main__":
    main()
