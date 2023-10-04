#!/usr/bin/env python3

import sys, re
from ete3 import Tree
from colour import Color
import matplotlib.colors as mcolors

def generate_n_colors(colors, color_num):
    by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                         name)
                        for name, color in colors.items())
    names = []
    for hsv, name in by_hsv:
        if not (hsv[1] < 0.25 and hsv[2] > 0.75) and hsv[2] > 0.25:
            names.append(name)
    subset_hex = []
    if len(names) > color_num:
        step = len(names) // color_num
        for i in range(0,len(names), step):
            subset_hex.append(mcolors.to_hex(colors[names[i]]))
    return subset_hex[:color_num]

if len(sys.argv) < 2:
    print("Usage: program <tsv with taxa 1st> > color_config")
    sys.exit(1)

taxa_tsv = sys.argv[1]

tree_config_cols = []
unique_labels = []
with open(taxa_tsv, "r") as fp:
    for line in fp:
        tmp = line.strip().split("\t")
        tree_config_cols.append([tmp[0], " ".join([tmp[0],tmp[1]])])
        if not tmp[1] in unique_labels:
            unique_labels.append(tmp[1])

config_colors = generate_n_colors(mcolors.XKCD_COLORS, len(unique_labels))
config_colors_ulabel = {}
for i, ulabel in enumerate(unique_labels):
    config_colors_ulabel[ulabel] = config_colors[i]

for line in tree_config_cols:
    tlabel = " ".join(line[-1].rsplit(" ")[1:])
    print(line[0], config_colors_ulabel[tlabel], line[1], sep="\t")
