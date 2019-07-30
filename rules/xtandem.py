# XTandem:
if config["digestion"]["tryptic"] == 'semi':
    xtandem_tryptic = '-semi_cleavage'
else: 
    xtandem_tryptic = ''

print(config["modifications"]["fixed"])

if config["modifications"]["fixed"] is None:
    fm = ""
elif len(config["modifications"]["fixed"]) < 1 :
    fm = ""
else: 
    fm = "-fixed_modifications {0}".format(' '.join('"{0}"'.format(w) for w in config["modifications"]["fixed"]))
print (fm)



print(config["modifications"]["variable"])

if config["modifications"]["variable"] is None:
    vm = ""
elif len(config["modifications"]["variable"]) < 1 :
    vm = ""
else: 
    vm = "-variable_modifications {0}".format(' '.join('"{0}"'.format(w) for w in config["modifications"]["variable"]))
print (vm)


rule xtandem:
    input:
        mzml = "mzml/{datafile}.mzML",
        fasta = 'work/database/target_decoy_database.fasta',
    output:
        idxml = "work/xtandem/{datafile}/dbsearch_{datafile}.idXML"
    singularity:
        config['singularity']['default']
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    threads: 4
    benchmark:
        "work/xtandem/{datafile}/dbsearch_{datafile}.benchmark.txt"
    params:
        pmt = "-precursor_mass_tolerance {0}".format(config["precursor"]["tolerance"]),
        pmu = "-precursor_error_units {0}".format(config["precursor"]["units"]),
        fmt = "-fragment_mass_tolerance {0}".format(config["fragment"]["tolerance"]),
        fmu = "-fragment_error_units {0}".format(config["fragment"]["units"]),
        e = "-enzyme {0}".format(config["digestion"]["enzyme"]),
        mc = "-missed_cleavages {0}".format(config["digestion"]["missed_cleavages"]),
        fm = fm,
        vm = vm,
        debug = '-debug {0}'.format(config["debug"]),
        tryptic = xtandem_tryptic,
        log = 'work/xtandem/{datafile}/dbsearch_{datafile}.log'
    shell:
        "XTandemAdapter "
        "-in {input.mzml} "
        "-out {output.idxml} "
        "-database {input.fasta} "
        "-xtandem_executable ./bin/XTandem/tandem_vengence "
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
