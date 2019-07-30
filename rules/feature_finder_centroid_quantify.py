#MapAlignerPoseClustering:
rule align_ffc_maps:
    input:
        featurexmls = expand("work/{{dbsearchdir}}/{sample}/ffc_ff_filt_idmap_{sample}.featureXML",sample=SAMPLES)
    output:
        featurexmls =
        temp(expand("work/{{dbsearchdir}}/{sample}/ffc_ff_filt_idmap_align_{sample}.featureXML",sample=SAMPLES))
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        'work/{dbsearchdir}/ffc_ff_filt_idmap_align_.benchmark.txt'
    params:
        mz_max_difference = "-algorithm:pairfinder:distance_MZ:max_difference {0}".format(config["precursor"]["tolerance"]),
        mz_unit = "-algorithm:pairfinder:distance_MZ:unit {0}".format(config["precursor"]["units"]),
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/ffc_ff_filt_idmap_align_.log'
    shell:
        "MapAlignerPoseClustering "
        "-in {input.featurexmls} "
        "-out {output.featurexmls} "
        "-threads {threads} "
        "{params.mz_max_difference} "
        "{params.mz_unit} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

#FeatureLinkerUnlabeledQT:
rule link_ffc_maps:
    input:
        featurexmls = expand("work/{{dbsearchdir}}/{sample}/ffc_ff_filt_idmap_align_{sample}.featureXML",sample=SAMPLES)
    output:
        featurexml = temp("work/{dbsearchdir}/ffc_ff_flq.consensusXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        'work/{dbsearchdir}/ffc_ff_flq.benchmark.txt'
    params:
        mz_max_difference = "-algorithm:distance_MZ:max_difference 20",
        mz_unit = "-algorithm:distance_MZ:unit ppm",
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/ffc_ff_flq.log'
    shell:
        "FeatureLinkerUnlabeledQT "
        "-in {input.featurexmls} "
        "-out {output.featurexml} "
        "-threads {threads} "
        "{params.mz_max_difference} "
        "{params.mz_unit} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

#IDConflictResolverRule
rule resolve_ffc_map_conflicts:
    input:
        featurexml = "work/{dbsearchdir}/ffc_ff_flq.consensusXML"
    output:
        featurexml = temp("work/{dbsearchdir}/ffc_ff_flq_idcr.consensusXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        'work/{dbsearchdir}/ffc_ff_flq_idcr.benchmark.txt'
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/ffc_ff_flq_idcr.log'
    shell:
        "IDConflictResolver "
        "-in {input.featurexml} "
        "-out {output.featurexml} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

#ConsensusMapNormalizer:
rule normalize_ffc_maps:
    input:
        featurexml = "work/{dbsearchdir}/ffc_ff_flq_idcr.consensusXML"
    output:
        featurexml = temp("work/{dbsearchdir}/ffc_ff_flq_idcr_cmn.consensusXML")
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads:
        2
    benchmark:
        'work/{dbsearchdir}/ffc_ff_flq_idcr_cmn.benchmark.txt'
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/ffc_ff_flq_idcr_cmn.log'
    shell:
        "ConsensusMapNormalizer "
        "-in {input.featurexml} "
        "-out {output.featurexml} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# ProteinQuantifier
rule quantify_proteins_ffc_maps:
    input:
        featurexml = "work/{dbsearchdir}/ffc_ff_flq_idcr_cmn.consensusXML",
        fido = "work/{dbsearchdir}/proteinid/fp_idf_2.idXML"
    output:
        csv = "csv/ffc_ff_{dbsearchdir}_proteinIntensities.csv"
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        'csv/ffc_ff_{dbsearchdir}_proteinIntensities.txt'
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "csv/ffc_ff_{dbsearchdir}_proteinIntensities.log"
    shell:
        "ProteinQuantifier "
        "-in {input.featurexml} "
        "-protein_groups {input.fido} "
        "-out {output.csv} "
        "-top 0 "
        "-average sum "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "
