# IDFilter
# Remove unmatched peptides (decoys)
rule ffidm_filter_ids_by_peptide_fdr:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/fdr_{datafile}.idXML"
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/ffidm_filt_{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/ffidm_filt_{datafile}.benchmark.txt"
    params:
        pepfdr = '-score:pep {0}'.format(config["peptide"]["fdr"]),
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/ffidm_filt_{datafile}.log'
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

rule ffidm_align_ids_per_sample:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/ffidm_filt_{datafile}.idXML",
        idxmls = expand("work/{{dbsearchdir}}/{sample}/ffidm_filt_{sample}.idXML",sample=SAMPLES)
    output:
        idxmls = temp(expand("work/{{dbsearchdir}}/{{datafile}}/ffidm_mapaligned_{sample}.idXML",sample=SAMPLES))
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/ffidm_mapaligned_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/ffidm_mapaligned_{datafile}.log'
    shell:
        "MapAlignerIdentification "
        "-in {input.idxmls} "
        "-out {output.idxmls} "
        "-reference:file {input.idxml} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# IDMerge
rule ffidm_merge_aligned_ids_per_sample:
    input:
        idxmls = expand("work/{{dbsearchdir}}/{{datafile}}/ffidm_mapaligned_{sample}.idXML",sample=SAMPLES)
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/ffidm_mapaligned_merged_{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/ffidm_mapaligned_merged_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "work/{dbsearchdir}/{datafile}/ffidm_mapaligned_merged_{datafile}.log"
    shell:
        "IDMerger "
        "-in {input.idxmls} "
        "-out {output.idxml} "
        "-annotate_file_origin "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FeatureFinderIdentification
rule ffidm:
    input:
        mzml = "mzml/{datafile}.mzML",
        idxml = "work/{dbsearchdir}/{datafile}/ffidm_mapaligned_merged_{datafile}.idXML",
    output:
        featurexml = "work/{dbsearchdir}/{datafile}/ffidm_{datafile}.featureXML"
    singularity:
        "shub://mafreitas/singularity-openms:latest"
    threads: 2
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/{datafile}/ffidm_{datafile}.benchmark.txt"
    params:
        lc_peak_width = "-detect:peak_width {0}".format(config["lc"]["peak_width"]),
        model_type = "-model:type {0}".format("none"),
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/ffidm_{datafile}.log'
    shell:
        "FeatureFinderIdentification "
        "-in {input.mzml} "
        "-id {input.idxml} "
        "-out {output.featurexml} "
        "{params.lc_peak_width} "
        "{params.model_type} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

#MapAlignerPoseClustering:
rule ffidm_align_maps:
    input:
        featurexmls = expand("work/{{dbsearchdir}}/{sample}/ffidm_{sample}.featureXML",sample=SAMPLES)
    output:
        featurexmls =
        temp(expand("work/{{dbsearchdir}}/{sample}/ffidm_final_cluster_{sample}.featureXML",sample=SAMPLES))
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/ffidm_final_cluster.benchmark.txt"
    params:
        mz_max_difference = "-algorithm:pairfinder:distance_MZ:max_difference 20",
        mz_unit = "-algorithm:pairfinder:distance_MZ:unit ppm",
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/ffidm_final_cluster.log'
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
rule ffidm_link_maps:
    input:
        featurexmls = expand("work/{{dbsearchdir}}/{sample}/ffidm_final_cluster_{sample}.featureXML",sample=SAMPLES)
    output:
        featurexml =
        temp("work/{dbsearchdir}/ffidm_flq.consensusXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/ffidm_flq.benchmark.txt"
    params:
        mz_max_difference = "-algorithm:distance_MZ:max_difference 20",
        mz_unit = "-algorithm:distance_MZ:unit ppm",
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/ffidm_flq.log'
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
rule ffidm_resolve_map_conflicts:
    input:
        featurexml = "work/{dbsearchdir}/ffidm_flq.consensusXML"
    output:
        featurexml = temp("work/{dbsearchdir}/ffidm_flq_idcr.consensusXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/ffidm_flq_idcr.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/ffidm_flq_idcr.log'
    shell:
        "IDConflictResolver "
        "-in {input.featurexml} "
        "-out {output.featurexml} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

#ConsensusMapNormalizer:
rule ffidm_normalize_maps:
    input:
        featurexml = "work/{dbsearchdir}/ffidm_flq_idcr.consensusXML"
    output:
        featurexml = temp("work/{dbsearchdir}/ffidm_flq_idcr_cmn.consensusXML")
    singularity:
        config['singularity']['default']
    threads: 4
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/{dbsearchdir}/ffidm_flq_idcr_cmn.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/ffidm_flq_idcr_cmn.log'
    shell:
        "ConsensusMapNormalizer "
        "-in {input.featurexml} "
        "-out {output.featurexml} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# ProteinQuantifier
rule ffidm_quantify_proteins:
    input:
        featurexml = "work/{dbsearchdir}/ffidm_flq_idcr_cmn.consensusXML",
        fido = "work/{dbsearchdir}/proteinid/fido_fdr_filt.idXML"
    output:
        csv = "csv/ffidm_{dbsearchdir}_proteinIntensities.csv"
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "csv/ffidm_{dbsearchdir}_proteinIntensities.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "csv/ffidm_{dbsearchdir}_proteinIntensities.log"
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
