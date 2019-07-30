# tsv pep only output

rule csv_idfilter_fdr:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/fdr_{datafile}.idXML"
    output:
        idxml = "work/{dbsearchdir}/{datafile}/fdr_idflt_pep_{datafile}.idXML"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "work/{dbsearchdir}/{datafile}/{datafile}/fdr_idflt_pep_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearchdir}/{datafile}/{datafile}/fdr_idflt_pep_{datafile}.log"
    shell:
        "IDFilter "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-score:pep 0.05 "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

rule csv_fdr_export:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/fdr_idflt_pep_{datafile}.idXML"
    output:
        csv = "csv/{dbsearchdir}/{datafile}/fdr_csv_{datafile}.csv"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    priority: 90
    benchmark:
        "csv/{dbsearchdir}/{datafile}/fdr_csv_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "csv/{dbsearchdir}/{datafile}/fdr_csv_{datafile}.log"
    shell:
        "TextExporter "
        "-in {input.idxml} "
        "-out {output.csv} "
        "-id:peptides_only "
        "-separator ',' "
        "-replacement ';' "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "
