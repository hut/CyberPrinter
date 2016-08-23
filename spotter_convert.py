#!/usr/bin/python

import sys

import argparse
parser = argparse.ArgumentParser(description='')
parser.add_argument('image_file', type=str)
args = parser.parse_args()

from PIL import Image
im = Image.open(args.image_file) #Can be many different formats.
pixels = im.load()


def get_color(colortuple):
    avg = (colortuple[0] + colortuple[1] + colortuple[2]) / 3
    if avg < 128:
        return 1 # black
    return 0 # white

def make_spotfile(spots):
    header = """mtp = MTP_Sys
group = iGEM
resetWells
resetSpots"""
    footer = "end"
    return "\n".join([header] + all_lines + [footer])

class Line(object):
    def __init__(self):
        self.maxlen = 255
        self.content = "t A1  "
        self.count = 0

    def add(self, x, y):
        # add 1 to each coordinate, as AFAIK the program starts counting at 1
        new_coord = " %d,%d" % (x + 1, y + 1)
        if len(self.content) + len(new_coord) > self.maxlen:
            raise ValueError("Line too long, refusing to add coordinate")
        self.content += new_coord
        self.count += 1

all_lines = []
line = Line()

for x in range(im.size[0]):
    for y in range(im.size[1]):
        color = get_color(pixels[x, y])
        if color:
            try:
                line.add(x, y)
            except ValueError:
                all_lines.append(line.content)
                line = Line()
if line.count > 0:
    all_lines.append(line.content)

spotfile = make_spotfile(all_lines)
spotfile = spotfile.replace("\n", "\r\n") # Windows Line Endings
print(spotfile)
