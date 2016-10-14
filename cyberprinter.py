#!/usr/bin/python

import sys

import argparse
parser = argparse.ArgumentParser(description='')
parser.add_argument('image_file', type=str)
args = parser.parse_args()

from PIL import Image
im = Image.open(args.image_file) #Can be many different formats.
pixels = im.load()
max_y = im.size[1] - 1


def get_color(colortuple):
    avg = (colortuple[0] + colortuple[1] + colortuple[2]) / 3
    if avg < 128:
        return 1 # black
    return 0 # white

def make_spotfile(spots):
    maxlen = 254
    lines = []
    linestart = "t A1  "
    header = """mtp = MTP_Sys
group = Katja_2
resetWells
resetSpots"""
    footer = "end"
    result = ""
    line_lengthtest = line = linestart
    for spot in spots:
        line_lengthtest += " " + str(spot)
        if len(line_lengthtest) > maxlen:
            lines.append(line + "\n")
            line_lengthtest = line = linestart + " " + str(spot)
        else:
            line = line_lengthtest
    if line != linestart:
        lines.append(line + "\n")

    first = True
    for line in lines:
        if first:
            first = False
        else:
            result += "\n\n\n\n"
        result += header
        result += line
        result += footer

    result = result.replace("\n", "\r\n") # Windows Line Ending
    return result

class Line(object):
    def __init__(self):
        self.maxlen = 255
        self.content = "t A1  "
        self.count = 0
        self.spots = []

    def get_line(self):
        return "t A1   " + " ".join(self.format_spot(spot) for spot in self.spots)

    def add(self, x, y):
        # add 1 to each coordinate, as AFAIK the program starts counting at 1
        spot = [x + 1, y + 1, 0, 0]
        if len(self.content) + len(new_coord) > self.maxlen:
            raise ValueError("Line too long, refusing to add coordinate")
        self.content += new_coord
        self.count += 1

class Spot(list):
    def _get_start_x(self): return self[0]
    def _set_start_x(self, value): self[0] = value
    def _get_stop_x(self): return self[1]
    def _set_stop_x(self, value): self[1] = value
    startx = property(_get_start_x, _set_start_x)
    stopx = property(_get_stop_x, _set_stop_x)
    def _get_start_y(self): return self[2]
    def _set_start_y(self, value): self[2] = value
    def _get_stop_y(self): return self[3]
    def _set_stop_y(self, value): self[3] = value
    starty = property(_get_start_y, _set_start_y)
    stopy = property(_get_stop_y, _set_stop_y)
    def __str__(self):
        out = ""
        if self.startx == self.stopx:
            out += str(self.startx)
        else:
            out += "%d:%d" % (self.startx, self.stopx)
        out += ','
        if self.starty == self.stopy:
            out += str(self.starty)
        else:
            out += "%d:%d" % (self.starty, self.stopy)
        return out

def reduce2(function, sequence):
    result = [sequence[0]]
    index = 1
    for item in sequence[1:]:
        a, b = result[-1], item
        del result[-1]
        result.extend(function(a, b))
    return result

def squash_along_y(spot1, spot2):
    if spot1.startx == spot2.startx and spot1.stopx == spot2.stopx and spot1.stopy == spot2.starty - 1:
        return [Spot([spot1.startx, spot1.stopx, spot1.starty, spot2.stopy])]
    else:
        return [spot1, spot2]

def squash_along_x(spot1, spot2):
    if spot1.starty == spot2.starty and spot1.stopy == spot2.stopy and spot1.stopx == spot2.startx - 1:
        return [Spot([spot1.startx, spot2.stopx, spot1.starty, spot1.stopy])]
    else:
        return [spot1, spot2]

spots = []

for x in range(im.size[0]):
    for y in range(im.size[1]):
        color = get_color(pixels[x, max_y - y])
        if color:
            spots.append(Spot([x, x, y, y]))

#print(" ".join(map(str, spots)))
#print()
#print()
#print(" ".join(map(str, reduce2(squash_along_y, spots))))
#print()
#print()
#print(" ".join(map(str, reduce2(squash_along_x, reduce2(squash_along_y, spots)))))

squashed_along_y = reduce2(squash_along_y, spots)
squashed_along_y.sort(key=lambda spot: (spot.starty, spot.stopy, spot.startx, spot.stopx))
squashed_spots = reduce2(squash_along_x, squashed_along_y)

print(make_spotfile(squashed_spots))
