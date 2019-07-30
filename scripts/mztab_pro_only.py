#!/usr/bin/env python
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

print ("Creating Protein tsv from mztab: {} -> {}".format(input_file, output_file))

with open(output_file,'w') as outfile:
    with open(input_file, 'r') as infile:
        for line in infile:
            if line.startswith("PRH\t") or \
                line.startswith("PRT\t"):
                outfile.write(line)
