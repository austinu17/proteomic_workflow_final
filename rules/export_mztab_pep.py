# IDFilter
rule mztab_pep_export:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/idpep_{datafile}.idXML"
    output:
        tsv = "mztab/{dbsearchdir}/{datafile}/pep_mztab_{datafile}.mzTab"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearchdir}/{datafile}/pep_mztab_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearchdir}/{datafile}/pep_mztab_{datafile}.log"
    shell:
        "MzTabExporter "
        "-in {input.idxml} "
        "-out {output.tsv} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# mztab_fdr_peponly_export
rule mztab_pep_peponly_export:
    input:
        tsv = "mztab/{dbsearchdir}/{datafile}/pep_mztab_{datafile}.mzTab"
    output:
        csv = "mztab/{dbsearchdir}/{datafile}/pep_mztab_peponly_{datafile}.mzTab"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearchdir}/{datafile}/pep_mztab_peponly_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearchdir}/{datafile}/pep_mztab_peponly_{datafile}.log"
    shell:
        "python3 scripts/mztab_pep_only.py "
        "{input.tsv} "
        "{output.csv}"