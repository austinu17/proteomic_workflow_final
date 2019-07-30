# IDFilter
# Remove unmatched peptides (decoys)
rule filter_peptides_ffi:
    input:
        idxml = rules.peptide_fdr.output.idxml #"work/{dbsearchdir}/{datafile}/fdr_{datafile}.idXML"
    output:
        idxml = "work/{dbsearchdir}/{datafile}/ffidi_fdr_filt_{datafile}.idXML"
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/pi_filt_ur_{datafile}.benchmark.txt"
    params:
        pepfdr = '-score:pep {0}'.format(config["peptide"]["fdr"]),
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/pi_filt_ur_{datafile}.log'
    shell:
        "IDFilter "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "{params.pepfdr} "
        "-score:prot 0 "
        "-delete_unreferenced_peptide_hits "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FeatureFinderIdentification
rule pep_ffi:
    input:
        mzml = "mzml/{datafile}.mzML",
        idxml = rules.filter_peptides_ffi.output.idxml # "work/{dbsearchdir}/{datafile}/ffidi_fdr_filt_{datafile}.idXML",
    output:
        featurexml = "work/{dbsearchdir}/{datafile}/ffidi_filt_{datafile}.featureXML",
        mzml = "work/{dbsearchdir}/{datafile}/ffidi_filt_{datafile}.mzml"
    singularity:
        "shub://mafreitas/singularity-openms:latest"
    threads: 2
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/ffidi_filt_{datafile}.benchmark.txt"
    params:
        lc_peak_width = "-detect:peak_width {0}".format(config["lc"]["peak_width"]),
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/ffidi_filt_{datafile}.log'
    shell:
        "FeatureFinderIdentification "
        "-in {input.mzml} "
        "-id {input.idxml} "
        "-out {output.featurexml} "
        "-chrom_out {output.mzml} " 
        "{params.lc_peak_width} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# IDFilter
rule mztab_pep_ffi_export:
    input:
        featurexml = rules.pep_ffi.output.featurexml 
    output:
        tsv = "mztab/{dbsearchdir}/{datafile}/pep_ffi_{datafile}.tsv"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearchdir}/{datafile}/pep_ffi_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearchdir}/{datafile}/pep_ffi_{datafile}.log"
    shell:
        "MzTabExporter "
        "-in {input.featurexml} "
        "-out {output.tsv} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# mztab_fdr_peponly_export
rule mztab_pep_ffi_peponly_export:
    input:
        tsv = rules.mztab_pep_ffi_export.output.tsv  
    output:
        tsv = "mztab/{dbsearchdir}/{datafile}/pep_ffi_peponly_{datafile}.tsv"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearchdir}/{datafile}/pep_ffi_peponly{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearchdir}/{datafile}/pep_ffi_peponly{datafile}.log"
    shell:
        "python3 scripts/mztab_pep_only.py "
        "{input.tsv} "
        "{output.tsv}"

# ffi_image
rule ffi_image:
    input:
        mzml = "mzml/{datafile}.mzML",
        featurexml = "work/{dbsearchdir}/{datafile}/ffidi_filt_{datafile}.featureXML"
    output:
        png = "plots/{dbsearchdir}/{datafile}/ffi_image_{datafile}.png"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "plots/{dbsearchdir}/{datafile}/ffi_image_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "plots/{dbsearchdir}/{datafile}/ffi_image_{datafile}.log"
    shell:
        "ImageCreator "
        "-in {input.mzml} "
        "-in_featureXML {input.featurexml} "
        "-out {output.png} "
        "-out_type png "
        "-width 4096 -height 4096 -precursors "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "
