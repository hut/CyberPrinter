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
    content = []
    for partition in zip(*[iter(spots)]*10):
        content.append("t A1   " + " ".join("%d,%d" % spot for spot in partition))
    return "\n".join([header] + content + [footer])

spots = []

for x in range(im.size[0]):
    for y in range(im.size[1]):
        color = get_color(pixels[x, y])
        if color:
            spots.append((x + 1, y + 1))  # the program starts counting at 1, AFAIK


spotfile = make_spotfile(spots)
spotfile = spotfile.replace("\n", "\r\n") # Windows Line Endings
print(spotfile)
