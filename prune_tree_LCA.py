#!/usr/bin/env python3.6

import sys
import os
import re
import argparse
from ete3 import Tree

def find_closest_sister_leaf(selected_node):
    if selected_node.is_root():
        # if selected_node was root there is no lca
        return selected_node
    lca = selected_node.up
    for child in lca.children:
        if child != selected_node:
            if child.is_leaf():
                return child
            else:
                return child.get_closest_leaf()[0]

def find_closest_aunt_leaf(selected_node):
    lca = selected_node.up
    return find_closest_sister_leaf(lca)

def wanted_taxa(name, taxalist, pattern):
    if taxalist:
        if name in taxalist:
            return True
    else:
        if pattern is not None:
            m = re.fullmatch(pattern, name, flags=0)
            if m is not None:
                return True
    return False

# Parse command line options
parser = argparse.ArgumentParser(
    description='Trim tree')
parser.add_argument(
   '-o',
   dest="ofix",
   required=True,
   help='Output prefix')
parser.add_argument(
    '-s',
    dest="filelist",
    help='Opt list of taxa')
parser.add_argument(
    '-p',
    dest="pattern",
    help='Opt python regex pattern for taxa names to keep, fx [a-z]{4}')
parser.add_argument(
    '-t',
    dest="treefile",
    required=True,
    help='Input phylogenic tree')
args = parser.parse_args()

# read sample accessions from first col of a tsv/lst
user_samples = []
if args.filelist is not None:
    with open(args.filelist, "r") as fp:
        for line in fp:
            user_samples.append(line.strip())

# load the tree to prune
tree = Tree(args.treefile, format=1, quoted_node_names=True)

# find the nodes to keep and their closest sisters/aunts
kept_nodes = []
for node in tree.traverse():
    if node.name:
        # inner nodes can also have names
        if wanted_taxa(node.name, user_samples, args.pattern):
            kept_nodes.append(node)
            # find sister
            sister_node = find_closest_sister_leaf(node)
            if sister_node is not None:
                kept_nodes.append(sister_node)
            # find aunt
            aunt_node = find_closest_aunt_leaf(node)
            if aunt_node is not None:
                kept_nodes.append(aunt_node)

# prune tree
tree.prune(kept_nodes, preserve_branch_length=True)

# save tree
tree.write(format=1, outfile=f"{args.ofix}.nwk")

sys.exit(0)
