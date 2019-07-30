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
# fp_idf
rule fp_idf:
    input:
        idxml = "work/{dbsearch}/proteinid/fp_idm.idXML",
    output:
        idxml = temp("work/{dbsearch}/proteinid/fp_idf.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearch}/proteinid/fp_idf.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearch}/proteinid/fp_idf.log"
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
        idxml = "work/{dbsearch}/proteinid/fp_idf.idXML"
    output:
        idxml = "work/{dbsearch}/proteinid/fp_fda.idXML"
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

# FP IDFilter
# fp_idf
rule fp_idf:
    input:
        idxml = "work/{dbsearch}/proteinid/fp_fdr.idXML"
    output:
        idxml = "work/{dbsearch}/proteinid/fp_idf.idXML"
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearch}/proteinid/fp_idf.benchmark.txt"
    params:
        profdr = '-score:prot {0}'.format(config["protein"]["fdr"]),
        pepfdr = '-score:pep {0}'.format(config["peptide"]["fdr"]),
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearch}/proteinid/fp_idf.log"
    shell:
        "IDFilter "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "{params.profdr} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# Export
rule mztab_fido_export:
    input:
        idxml = "work/{dbsearch}/proteinid/fido_fdr_filt.idXML"
    output:
        tsv = "mztab/{dbsearch}/fido_fdr_filt.mzTab"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearch}/fido_fdr_filt.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearch}/fido_fdr_filt.log"
    shell:
        "MzTabExporter "
        "-in {input.idxml} "
        "-out {output.tsv} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# export_fido_fdr_protein_list
rule export_fido_fdr_protein_list:
    input:
        tsv = "mztab/{dbsearch}/fido_fdr_filt.mzTab"
    output:
        tsv = "mztab/{dbsearch}/fido_fdr_filt_prot_only.mzTab"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearch}/fido_fdr_filt_prot_only.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearch}/fido_fdr_filt_prot_only.log"
    shell:
        "python3 scripts/mztab_pro_only.py "
        "{input.tsv} "
        "{output.tsv} "
        "2>&1 | tee {params.log} "
