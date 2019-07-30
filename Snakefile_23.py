import errno, glob, os, os.path, sys

shell.prefix('')
configfile: "config.yaml"

# SAMPLES = list()
# RAWFILES = glob.glob("{0}/*".format(config["raw"]["location"]))
# allowed_exts = [".raw",".RAW"]
# for rawfile in RAWFILES:
#     rbase = os.path.basename(rawfile)
#     rbase,rext = os.path.splitext(rbase)
#     if rext in allowed_exts:
#         SAMPLES.append(rbase)

SAMPLES = list()
#print("{0}/*".format(config["mzml"]["location"]))
MZMLFILES = glob.glob("{0}/*".format(config["mzml"]["location"]))
#print(MZMLFILES)
allowed_exts = [".mzML",".MZML",".mzml"]
for rawfile in MZMLFILES:
    rbase = os.path.basename(rawfile)
    rbase,rext = os.path.splitext(rbase)
    if rext in allowed_exts:
        SAMPLES.append(rbase)

DBFILES = glob.glob("{0}/*".format(config["fasta"]["location"]))
DATABASES = []
allowed_exts = [".fasta",".FASTA"]
for dbfile in DBFILES:
    dbase = os.path.basename(dbfile)
    dbase,dext = os.path.splitext(dbase)
    if dext in allowed_exts:
        DATABASES.append(dbase)

# Setup Targets for Pipeline
rule targets:
    input:
         "work/database/target_decoy_database.fasta",
        #  expand("mztab/{dbsearch}/{sample}/fdr_mztab_{sample}.tsv",
        #     dbsearch=config["search_engines"],sample=SAMPLES),
        #  expand("csv/{dbsearch}/{sample}/fdr_csv_{sample}.csv",
        #     dbsearch=config["search_engines"],sample=SAMPLES),
        #  expand("mztab/{dbsearch}/{sample}/pep_mztab_{sample}.tsv",
        #     dbsearch=config["search_engines"],sample=SAMPLES),
        #  expand("csv/{dbsearch}/{sample}/pep_csv_{sample}.csv",
        #     dbsearch=config["search_engines"],sample=SAMPLES),
        #  expand("mztab/{dbsearch}/{sample}/fdr_mztab_peponly_{sample}.tsv",
        #     dbsearch=config["search_engines"],sample=SAMPLES),
        #  expand("mztab/{dbsearch}/{sample}/pep_mztab_peponly_{sample}.tsv",
        #     dbsearch=config["search_engines"],sample=SAMPLES),
        #  expand("mztab/{dbsearch}/{sample}/pep_ffi_peponly_{sample}.tsv",
        #     dbsearch=config["search_engines"],sample=SAMPLES),
        #  expand("plots/{dbsearch}/{sample}/ffi_image_{sample}.png",
        #     dbsearch=config["search_engines"],sample=SAMPLES),
         expand("csv/sc_{dbsearch}_proteinCounts.csv", dbsearch=config["search_engines"]),
#        expand("csv/ffm_{dbsearch}_proteinIntensities.csv", dbsearch=config["search_engines"]),
#        expand("csv/ffc_{dbsearch}_proteinIntensities.csv", dbsearch=config["search_engines"]),
         expand("csv/ffidi_{dbsearch}_proteinIntensities.csv", dbsearch=config["search_engines"]),
         expand("mztab/{dbsearch}/fido_fdr_filt_prot_only.tsv", dbsearch=config["search_engines"]),
         
# Construct Concatenated Databases With Decoys
include: "rules/decoy_database.py"

# Remove Compression
#include: "rules/file_conversion_raw.py"

# Remove Compression
include: "rules/file_conversion_mzml.py"

# Perform Database Search
for search in config["search_engines"]:
    include: "rules/%s.py" % search

# Perfrom Post Processing of Database Searches
include: "rules/search_post_processing.py"

# Perfrom Export FDR MzTab
#include: "rules/export_mztab_fdr.py"

# Perfrom Export PEP MzTab
#include: "rules/export_mztab_pep.py"

# Perfrom Export FDR csv
#include: "rules/export_csv_fdr.py"

# Perfrom Export PEP csv
#include: "rules/export_csv_pep.py"

# Perform Protein Inference
include: "rules/fido.py"

# Perfrom Feature Finding
#include: "rules/feature_finder_id_pep.py"

# Perfrom Feature Finding
include: "rules/feature_finder_identification_internal.py"

# Perfrom Feature Finding
#include: "rules/feature_finder_multiplex.py"

# Perfrom Feature Finding
#include: "rules/feature_finder_centroid.py"

# Determine Spectral Counts
include: "rules/spectral_counts.py"

# Finalize script
include: "rules/onsuccess.py"
