# tsv pep only output

rule csv_pep_export:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/idpep_{datafile}.idXML"
    output:
        csv = "csv/{dbsearchdir}/{datafile}/pep_csv_{datafile}.csv"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    priority: 90
    benchmark:
        "csv/{dbsearchdir}/{datafile}/idpep_csv_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "csv/{dbsearchdir}/{datafile}/idpep_csv_{datafile}.log"
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
