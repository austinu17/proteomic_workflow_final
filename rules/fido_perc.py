# Fido Percolator 
# FP
#
# FP IDMerge
# fp_idm
rule fp_idm:
    input:
        idxmls = expand(
            "work/{{dbsearch}}/{sample}/sppp_idss_{sample}.idXML", sample=SAMPLES)
    output:
        idxml = temp("work/{dbsearch}/proteinid/fp_idm.idXML"),
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearch}/proteinid/fp_idm.benchmark.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearch}/proteinid/fp_idm.log"
    shell:
        "IDMerger "
        "-in {input.idxmls} "
        "-out {output.idxml} "
        "-annotate_file_origin "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FP IDFilter
# fp_idf_1
rule fp_idf_1:
    input:
        idxml = "work/{dbsearch}/proteinid/fp_idm.idXML",
    output:
        idxml = temp("work/{dbsearch}/proteinid/fp_idf_1.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearch}/proteinid/fp_idf_1.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearch}/proteinid/fp_idf_1.log"
    shell:
        "IDFilter "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-score:pep 1.0 "
        "-score:prot 0 "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FP FidoAdapter
# fp_fda 
rule fp_fda:
    input:
        idxml = "work/{dbsearch}/proteinid/fp_idf_1.idXML"
    output:
        idxml = temp("work/{dbsearch}/proteinid/fp_fda.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearch}/proteinid/fp_fda.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearch}/proteinid/fp_fda.log"
    shell:
        "FidoAdapter "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-fido_executable bin/Fido/Fido "
        "-fidocp_executable bin/Fido/FidoChooseParameters "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FP FalseDiscoveryRate
# fp_fdr
rule fp_fdr:
    input:
        idxml = "work/{dbsearch}/proteinid/fp_fda.idXML"
    output:
        idxml = temp("work/{dbsearch}/proteinid/fp_fdr.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearch}/proteinid/fp_fdr.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearch}/proteinid/fp_fdr.log"
    shell:
        "FalseDiscoveryRate "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-PSM false "
        "-protein true "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FP IDFilter Post Fido
# fp_idf_2
rule fp_idf_2:
    input:
        idxml = "work/{dbsearch}/proteinid/fp_fdr.idXML"
    output:
        idxml = temp("work/{dbsearch}/proteinid/fp_idf_2.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearch}/proteinid/fp_idf_2.benchmark.txt"
    params:
        profdr = '-score:prot {0}'.format(config["protein"]["fdr"]),
        pepfdr = '-score:pep {0}'.format(config["peptide"]["fdr"]),
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearch}/proteinid/fp_idf_2.log"
    shell:
        "IDFilter "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "{params.profdr} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FP Export All Results
# fp_results
rule fp_results:
    input:
        idxml = "work/{dbsearch}/proteinid/fp_idf_2.idXML"
    output:
        tsv = "mztab/{dbsearch}/fp_results.mzTab"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearch}/fp_results.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearch}/fp_results.log"
    shell:
        "MzTabExporter "
        "-in {input.idxml} "
        "-out {output.tsv} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FP Export Proteins
# fp_proteins
rule fp_proteins:
    input:
        tsv = "mztab/{dbsearch}/fp_results.mzTab"
    output:
        tsv = "mztab/{dbsearch}/fp_proteins.mzTab"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearch}/fp_proteins.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearch}/fp_proteins.log"
    shell:
        "python3 scripts/mztab_pro_only.py "
        "{input.tsv} "
        "{output.tsv} "
        "2>&1 | tee {params.log} "
