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

if len(sys.argv) < 3:
    print("Usage: program <list_of_taxa> <trees>")
    sys.exit(1)

#default color
color = "#84a1f4"

#get the taxa ids
taxaid_list = sys.argv[1]
if not os.path.exists(taxaid_list):
    sys.exit(1)
taxa_id = []
with open(taxaid_list, "r") as fp:
    for line in fp:
        taxa_id.append(line.strip())

# open nw in ete for node labels
tree_files = sys.argv[2:]
for tfile in tree_files:
    tr = Tree(tfile)
    no_tips = 0
    for node in tr.traverse("postorder"):
        if node.name:
            no_tips += 1

    new_tfile = os.path.join(os.path.dirname(tfile), "co_{}.clusters.nexus".format(os.path.basename(tfile).rsplit(".",1)[0]))
    with open(new_tfile, "w") as of:

        print("#NEXUS\nbegin taxa;", file=of)
        print("\tdimensions ntax={};\n\ttaxlabels".format(no_tips), file=of)
        for node in tr.traverse("postorder"):
            if node.name:
                if node.name[0] != "'" or node.name[0] != node.name[-1]:
                    if node.name.find("'") > -1:
                        node.name = node.name.replace("'","")
                    apostr_nn = "'{}'".format(node.name)
                else:
                    apostr_nn = node.name
                found = False
                for taxa_name in taxa_id:
                    if node.name.find(taxa_name) > -1:
                        print("\t{0}[&!color={1}]".format(apostr_nn, color), file=of)
                        print(taxa_name, node.name)
                        found = True
                        break
                if not found:
                    print("\t",apostr_nn, sep="", file=of)
                node.name = apostr_nn
        print(";\nend;", file=of)

        print("begin trees;\n\ttree tree_1 = [&R]", end=" ", file=of)
        print(tr.write(), file=of)
        print("end;", file=of)
