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
    print("Usage: program <trees>")
    sys.exit(1)

tfile = sys.argv[1]

# open nw in ete for node labels
tree_files = sys.argv[1:]
for tfile in tree_files:
    tr = Tree(tfile)
    # no of tips
    no_taxa = 0
    taxa = []
    for node in tr.traverse("postorder"):
        if node.name:
            no_taxa += 1
            taxa.append(node.name)
    new_tfile = os.path.join(os.path.dirname(tfile), "co_{}.nexus".format(os.path.basename(tfile).rsplit(".",1)[0]))

    # generate coloour scale and pair it with ST types
    taxa_colors = {}
    if no_taxa > 1:
        scl = generateColorGradient((50, 126, 193), (193, 50, 50), no_taxa)
        taxa_colors = { taxa[i]: scl[i] for i in range(no_taxa)}
    elif no_taxa == 1:
        scl = "#0000ff"
        taxa_colors = { taxa[0]: scl }
    else:
        sys.exit("No taxa found")

    with open(new_tfile, "w") as of:

        print("#NEXUS\nbegin taxa;", file=of)
        print("\tdimensions ntax={};\n\ttaxlabels".format(no_taxa), file=of)
        for node in tr.traverse("postorder"):
            if node.name:
                if node.name[0] != "'" or node.name[0] != node.name[-1]:
                    apostr_nn = "'{}'".format(node.name)
                else:
                    apostr_nn = node.name
                common = False
                for taxa_name in taxa:
                    if node.name.find(taxa_name) > -1:
                        print("\t{0}[&!color={1}]".format(apostr_nn, taxa_colors[taxa_name]), file=of)
                        common = True
                        break
                if not common:
                    print("\t",apostr_nn, sep="", file=of)
                node.name = apostr_nn
        print(";\nend;", file=of)

        print("begin trees;\n\ttree tree_1 = [&R]", end=" ", file=of)
        print(tr.write(), file=of)
        print("end;", file=of)
