# Search Post Processing Percolator
# SPPP

# SPPP Index peptides
# spp_ip
rule sppp_ip:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/dbsearch_{datafile}.idXML",
        fasta = 'work/database/target_decoy_database.fasta'
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/sppp_ip_{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/sppp_ip_{datafile}.benchmark.txt"
    params:
        decoy_string = "-decoy_string {0}".format(config["database"]["decoy_string"]),
        decoy_string_position = "-decoy_string_position {0}".format(config["database"]["decoy_string_position"]),
        missing_decoy_action = "-missing_decoy_action {0}".format(config["database"]["missing_decoy_action"]),
        enzyme = "-enzyme:name {0}".format(config["digestion"]["enzyme"]),
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/sppp_ip_{datafile}.log'
    shell:
        "PeptideIndexer "
        "-in {input.idxml} "
        "-fasta {input.fasta} "
        "-out {output.idxml} "
        "-allow_unmatched "
        "-IL_equivalent "
        "-enzyme:specificity none "
        "-threads {threads} "
        "{params.decoy_string} "
        "{params.decoy_string_position} "
        "{params.missing_decoy_action} "
        "{params.enzyme} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# SPPP PSMFeatureExtractor
# sppp_psmfe

rule sppp_psmfe:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/sppp_ip_{datafile}.idXML"
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/sppp_psmfe{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/sppp_psmfe{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/sppp_psmfe{datafile}.log'
    shell:
        "PSMFeatureExtractor "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# SPPP PercolatorAdapter
# sppp_perc
rule sppp_perc:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/sppp_psmfe{datafile}.idXML"
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/sppp_perc_{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/sppp_perc_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/sppp_perc_{datafile}.log'
    shell:
        "PercolatorAdapter "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-percolator_executable bin/Percolator/percolator "
        "-post-processing-tdc "
        "-subset-max-train 100000 "
        "-peptide-level-fdrs -protein-level-fdrs "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# SPPP FalseDiscoveryRate:
# sppp_fdr
rule sppp_fdr:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/sppp_perc_{datafile}.idXML"
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/sppp_fdr_t_{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/sppp_fdr_t_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/sppp_fdr_t_{datafile}.log'
    shell:
        "FalseDiscoveryRate "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-algorithm:add_decoy_peptides "
        "-algorithm:add_decoy_proteins "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "


# SPPP IDFilter:
# sppp_idf
rule sppp_idf:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/sppp_fdr_t_{datafile}.idXML"
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/sppp_fdr_{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/sppp_fdr_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/sppp_fdr_{datafile}.log'
    shell:
        "IDFilter "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-score:pep 0.05 "
        #"-score:prot 0 "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# IDScoreSwitcher:
# SPPP sppp_idss
rule sppp_idss:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/sppp_fdr_{datafile}.idXML"
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/sppp_idss_{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/sppp_idss_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/sppp_idss_{datafile}.log'
    shell:
        "IDScoreSwitcher "
        "-in {input.idxml} "
        "-out {output.idxml} "
        "-old_score q-value "
        "-new_score MS:1001493 "
        "-new_score_orientation lower_better "
        "-new_score_type \"Posterior Error Probability\" "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "