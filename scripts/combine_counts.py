import pandas as pd
import numpy as np
import glob
import os

files = sys.argv[1:]
df = pd.read_csv(files[0], sep="\t", skiprows=2)
colnames = df.columns

newnames = [colnames[0]]
for i in range(1, len(colnames)):
    name = colnames[i]
    newnames.append(params.names[0] + name)
df.columns = newnames

for i in range(1, len(files)):
    dft = pd.read_csv(files[i], sep="\t", skiprows=2)

    colnames = dft.columns
    newnames = [colnames[0]]
    for j in range(1, len(colnames)):
        name = colnames[j]
        newnames.append(params.names[i] + "_" + name)
    dft.columns = newnames

    df = pd.merge(df, dft, how="outer", on='protein')

df.to_csv(output.csv)
