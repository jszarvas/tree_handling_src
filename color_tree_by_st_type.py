#!/usr/bin/env python3

import sys, re, os
from ete3 import Tree
from colour import Color

# https://stackoverflow.com/questions/24016456/how-to-programmatically-create-n-sequential-equidistant-colors-ranging-from-dark
def generateColorGradient(RGB1, RGB2, n):
    '''
       red: generateColorGradient((103,0,13), (252,187,161), 20)
       blue: generateColorGradient((0,27,103), (181, 200, 255), 20)
    '''
    dRGB = [float(x2-x1)/(n-1) for x1, x2 in zip(RGB1, RGB2)]
    rgb_gradient = [tuple([int(x+k*dx) for x, dx in zip(RGB1, dRGB)]) for k in range(n)]
    gradient = [Color(rgb=(tpl[0]/255.0, tpl[1]/255.0, tpl[2]/255.0)).hex for tpl in rgb_gradient]
    return gradient

if len(sys.argv) < 2:
    print("Usage: program <tree> > colored_tree.newick")
    sys.exit(1)

cur_tfile = sys.argv[1]
rgb1 = (0,27,103)
rgb2 = (181, 200, 255)
if len(sys.argv) == 4:
    rgb1 = tuple([int(x) for x in sys.argv[2].split(",")])
    rgb2 = tuple([int(x) for x in sys.argv[3].split(",")])

# open nw file for getting the st_types
try:
    cur_tree = open(cur_tfile, "r")
except IOError as e:
    print(e, file=sys.stderr)
    sys.exit(1)

cur_nw = "".join(cur_tree.readlines())

cur_tree.close()

st_types = list(set(re.findall(r'ST_\d+', cur_nw)))
#print(st_types)
no_st_types = len(st_types)

# generate coloour scale and pair it with ST types
if no_st_types > 1:
    scl = generateColorGradient(rgb1, rgb2, no_st_types)
    st_colors = { st_types[i]: scl[i] for i in range(no_st_types)}
elif no_st_types == 1:
    scl = "#0000ff"
    st_colors = { st_types[0]: scl }
else:
    pass

# open nw in ete for node labels
tr = Tree(cur_tfile)

print("#NEXUS\nbegin taxa;")
print("\tdimensions ntax={};\n\ttaxlabels".format(len(re.findall(r'\*?C00\d+', cur_nw))+1))
for node in tr.traverse("postorder"):
    if node.name:
        apostr_nn = "'{}'".format(node.name)
        if node.name[0] == "'":
            apostr_nn = node.name
        if node.name.find("ST_") > -1:
            st_ty_m = re.search(r'ST_\d+', node.name)
            if st_ty_m:
                print("\t{0}[&!color={1}]".format(apostr_nn, st_colors[st_ty_m.group(0)]))
            else:
                print("\t",apostr_nn, sep="")
        else:
            print("\t",apostr_nn, sep="")
        node.name = apostr_nn
print(";\nend;")

print("begin trees;\n\ttree tree_1 = [&R]", end=" ")
print(tr.write())
print("end;")
