# myrimatch:

if config["digestion"]["tryptic"] == 'semi':
    myrimatch_tryptic = '-MinTerminiCleavages 1'
else: 
    myrimatch_tryptic = ''

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
rule myrimatch_search:
    input:
        mzml = "mzml/{datafile}.mzML",
        fasta = 'work/database/target_decoy_database.fasta',
    output:
        idxml = "work/myrimatch/{datafile}/dbsearch_{datafile}.idXML"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 32000
    threads: 4
    benchmark:
        "work/myrimatch/{datafile}/dbsearch_{datafile}.benchmark.txt"
    params:
        pmt = "-precursor_mass_tolerance {0}".format(config["precursor"]["tolerance"]),
        pmu = "-precursor_mass_tolerance_unit {0}".format(config["precursor"]["units"]),
        fmt = "-fragment_mass_tolerance {0}".format(config["fragment"]["tolerance"]),
        fmu = "-fragment_mass_tolerance_unit {0}".format(config["fragment"]["units"]),
        e = "-CleavageRules {0}".format(config["digestion"]["enzyme"]),
        mc = "-MaxMissedCleavages {0}".format(config["digestion"]["missed_cleavages"]),
        fm = fm,
        vm = vm,
        tryptic = myrimatch_tryptic,
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/myrimatch/{datafile}/dbsearch_{datafile}.log'
    shell:
        "MyriMatchAdapter "
        "-in {input.mzml} "
        "-out {output.idxml} "
        "-database {input.fasta} "
        "-myrimatch_executable bin/myrimatch/myrimatch_20190514 "
        "{params.pmt} "
        "{params.pmu} "
        "{params.fmt} "
        "{params.fmu} "
        "{params.e} "
        "{params.mc} "
        "{params.fm} "
        "{params.vm} "
        "{params.tryptic} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "
