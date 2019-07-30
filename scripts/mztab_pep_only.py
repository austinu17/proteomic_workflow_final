#!/usr/bin/env python
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

print ("Creating Peptide csv from mztab: {} -> {}".format(input_file, output_file))

with open(output_file,'w') as outfile:
    with open(input_file, 'r') as infile:
        for line in infile:
            if line.startswith("PSM\t") or \
                line.startswith("PSH\t") or \
                line.startswith("PEP\t") or \
                line.startswith("PEH\t"):
                outfile.write(line)