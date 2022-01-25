#!/usr/bin/env python3

import sys, re, os
from ete3 import Tree
from colour import Color

if len(sys.argv) < 3:
    print("Usage: program <taxa and color config> <trees>")
    sys.exit(1)

# get the taxa colors from the config file
cfi_file = sys.argv[1]
taxa_colors = {}
with open(cfi_file, "r") as fp:
    for line in fp:
        # common id    color_code
        tmp = line.strip().split("\t")
        taxa_colors[tmp[0]] = tmp[1]

# open nw in ete for node labels
tree_files = sys.argv[2:]
for tfile in tree_files:
    tr = Tree(tfile)
    # no of tips
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
                    apostr_nn = "'{}'".format(node.name)
                else:
                    apostr_nn = node.name
                common = False
                for taxa_name in taxa_colors.keys():
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
