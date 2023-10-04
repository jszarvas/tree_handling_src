#!/usr/bin/env python3

import os
import sys, re
from ete3 import Tree
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def order_mode(arg_mode):
    if arg_mode == "asc":
        return False
    else:
        return True

if len(sys.argv) < 3:
    print("Usage: program <asc|desc> <tree> <out prefix>")
    sys.exit(1)

# open nw in ete for branch lengths
bl_list = []
tr = Tree(sys.argv[2])
for node in tr.traverse("postorder"):
    bl_list.append(node.dist)

plt.hist(bl_list, bins=[0,0.01,0.05,0.1,0.5,1,2])
plt.savefig(f"{sys.argv[3]}.png", format="png")

bl_list.sort(reverse=order_mode(sys.argv[1]))
with open(f"{sys.argv[3]}.lst", "w") as op:
    for bl in bl_list:
        print(f"{bl:.6f}", file=op)
