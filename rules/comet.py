# Comet:
if config["modifications"]["fixed"] is None:
    fm = ""
elif len(config["modifications"]["fixed"]) < 1 :
    fm = ""
else: 
    fm = "-fixed_modifications {0}".format(' '.join('"{0}"'.format(w) for w in config["modifications"]["fixed"]))
print (fm)

if config["modifications"]["variable"] is None:
    vm = ""
elif len(config["modifications"]["variable"]) < 1 :
    vm = ""
else: 
    vm = "-variable_modifications {0}".format(' '.join('"{0}"'.format(w) for w in config["modifications"]["variable"]))
print (vm)


rule comet:
    input:
        mzml = "mzml/{datafile}.mzML",
        fasta = 'work/database/target_decoy_database.fasta',
    output:
        idxml = "work/comet/{datafile}/dbsearch_{datafile}.idXML"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 4
    benchmark:
        "work/comet/{datafile}/dbsearch_{datafile}.benchmark.txt"
    params:
        pmt = "-precursor_mass_tolerance {0}".format(config["precursor"]["tolerance"]),
        pmu = "-precursor_error_units {0}".format(config["precursor"]["units"]),
        e = "-enzyme {0}".format(config["digestion"]["enzyme"]),
        mc = "-allowed_missed_cleavages {0}".format(config["digestion"]["missed_cleavages"]),
        fm = fm,
        vm = vm,
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/comet/{datafile}/dbsearch_{datafile}.log'
    shell:
        "CometAdapter "
        "-in {input.mzml} "
        "-out {output.idxml} "
        "-database {input.fasta} "
        "-comet_executable bin/comet/201601/comet.exe "
        "{params.pmt} "
        "{params.pmu} "
        "{params.e} "
        "{params.mc} "
        "{params.fm} "
        "{params.vm} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "
