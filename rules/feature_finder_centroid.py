# FeatureFinderCentroided
rule find_features_centroid:
    input:
        mzml = "mzml/{datafile}.mzML"
    output:
        featurexml = "work/ffc_{datafile}.featureXML"
    threads: 6
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "work/ffc_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/ffc_{datafile}.log'
    singularity:
        config['singularity']['default']
    shell:
         "FeatureFinderCentroided "
         "-in {input.mzml} "
         "-out {output.featurexml} "
         "-algorithm:intensity:bins 100 "
         "-algorithm:mass_trace:mz_tolerance 0.1 "
         "-algorithm:mass_trace:max_missing 2 "
         "-algorithm:isotopic_pattern:mz_tolerance 0.1 "
         "-algorithm:isotopic_pattern:mass_window_width 5 "
         "-algorithm:seed:min_score 0.9 "
         "-algorithm:fit:max_iterations 50 "
         "-algorithm:feature:min_score 0.7 "
         "-algorithm:feature:min_isotope_fit 0.7 "
         "-algorithm:feature:min_trace_score 0.5 "
         "-algorithm:feature:min_rt_span 0.1 "
         "-algorithm:feature:rt_shape asymmetric "
         "-algorithm:feature:max_rt_span 5 "
         "-threads {threads} "
         "{params.debug} "
         "2>&1 | tee {params.log} "

# IDFilter
rule filter_features_by_intensity:
    input:
       featurexml = "work/ffc_{datafile}.featureXML"
    output:
        featurexml = "work/ffc_ff_{datafile}.featureXML"
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        'work/ffc_ff_{datafile}.benchmark.txt'
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/ffc_ff_{datafile}.log'
    shell:
        "FileFilter "
        "-in {input.featurexml} "
        "-out {output.featurexml} "
        "-f_and_c:remove_meta 'EGH_height' 'lt' 1e07 "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "



# FFC TextExporter 
# ffc_export_features_centroid
rule ffc_export:
    input:
        featurexml = "work/ffc_{datafile}.featureXML"
    output:
        csv = "csv/ffc_export_{datafile}.csv"
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "csv/ffc_export_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'csv/ffc_export_{datafile}.log'
    singularity:
        config['singularity']['default']
    shell:
         "TextExporter "
         "-in {input.featurexml} "
         "-out {output.csv} "
         "-threads {threads} "
         "{params.debug} "
         "2>&1 | tee {params.log} "

# FFC TextExporter 
# ffc_export_features_centroid
rule ffc_ff_export:
    input:
        featurexml = "work/ffc_ff_{datafile}.featureXML"
    output:
        csv = "csv/ffc_ff_export_{datafile}.csv"
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "csv/ffc_ff_export_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'csv/ffc_ff_export_{datafile}.log'
    singularity:
        config['singularity']['default']
    shell:
         "TextExporter "
         "-in {input.featurexml} "
         "-out {output.csv} "
         "-threads {threads} "
         "{params.debug} "
         "2>&1 | tee {params.log} "


# IDFilter
rule ffc_filt:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/sppp_fdr_{datafile}.idXML"
    output:
        idxml = temp("work/{dbsearchdir}/{datafile}/ffc_sppp_idf_filt_{datafile}.idXML")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        'work/{dbsearchdir}/{datafile}/ffc_sppp_idf_filt_{datafile}.benchmark.txt'
    params:
        pepfdr = '-score:pep {0}'.format(config["peptide"]["fdr"]),
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/ffc_sppp_idf_filt_{datafile}.log'
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

#IDMapper
rule ffc_filt_idmap:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/ffc_sppp_idf_filt_{datafile}.idXML",
        featurexml = "work/ffc_{datafile}.featureXML"
    output:
        featurexml = "work/{dbsearchdir}/{datafile}/ffc_filt_idmap_{datafile}.featureXML"
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        'work/{dbsearchdir}/{datafile}/ffc_filt_idmap_{datafile}.benchmark.txt'
    params:
        centroid_rt = "-feature:use_centroid_rt true",
        centroid_mz = "-feature:use_centroid_mz true",
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/ffc_filt_idmap_{datafile}.log'
    shell:
        "IDMapper "
        "-id {input.idxml} "
        "-in {input.featurexml} "
        "-out {output.featurexml} "
        "{params.centroid_rt} "
        "{params.centroid_mz} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

#IDMapper
rule ffc_ff_filt_idmap:
    input:
        idxml = "work/{dbsearchdir}/{datafile}/ffc_sppp_idf_filt_{datafile}.idXML",
        featurexml = "work/ffc_ff_{datafile}.featureXML"
    output:
        featurexml = "work/{dbsearchdir}/{datafile}/ffc_ff_filt_idmap_{datafile}.featureXML"
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        'work/{dbsearchdir}/{datafile}/ffc_ff_filt_idmap_{datafile}.benchmark.txt'
    params:
        centroid_rt = "-feature:use_centroid_rt true",
        centroid_mz = "-feature:use_centroid_mz true",
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/{dbsearchdir}/{datafile}/ffc_ff_filt_idmap_{datafile}.log'
    shell:
        "IDMapper "
        "-id {input.idxml} "
        "-in {input.featurexml} "
        "-out {output.featurexml} "
        "{params.centroid_rt} "
        "{params.centroid_mz} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FFC Export Mapped Features
# ffc_results
rule ffc_idm_results_:
    input:
        featurexml = "work/{dbsearchdir}/{datafile}/ffc_filt_idmap_{datafile}.featureXML"
    output:
        mztab = "mztab/{dbsearchdir}/{datafile}/ffc_idm_results_{datafile}.mzTab"
        
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearchdir}/{datafile}/ffc_ff_idm_results_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearchdir}/{datafile}/ffc_idm_results_{datafile}.log"
    shell:
        "MzTabExporter "
        "-in {input.featurexml} "
        "-out {output.mztab} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# FFC Export Mapped Features
# ffc_results
rule fp_ff_idm_results_:
    input:
        featurexml = "work/{dbsearchdir}/{datafile}/ffc_ff_filt_idmap_{datafile}.featureXML"
    output:
        mztab = "mztab/{dbsearchdir}/{datafile}/ffc_ff_idm_results_{datafile}.mzTab"
        
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 1
    benchmark:
        "mztab/{dbsearchdir}/{datafile}/ffc_ff_idm_results_{datafile}.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = "mztab/{dbsearchdir}/{datafile}/ffc_ff_idm_results_{datafile}.log"
    shell:
        "MzTabExporter "
        "-in {input.featurexml} "
        "-out {output.mztab} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "