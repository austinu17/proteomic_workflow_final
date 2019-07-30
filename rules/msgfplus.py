# MSGFPlusIndexDB:

if config["digestion"]["tryptic"] == 'semi':
    msgfplus_tryptic = '-tryptic semi'
else: 
    msgfplus_tryptic = ''

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


rule msgfplus_db_index:
    input:
        fasta = 'work/database/target_decoy_database.fasta'
    output:
        index = 'work/database/target_decoy_database.canno'
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 16000
    benchmark:
        "work/database/MSGFPlusIndexDB.benchmark.txt"
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/database/MSGFPlusIndexDB.log'
    shell:
        "java -Xmx3500M -cp "
        # "/usr/local/openms_thirdparty/All/MSGFPlus/MSGFPlus.jar "
        "bin/msgfplus/MSGFPlus_20190418.jar "
        "edu.ucsd.msjava.msdbsearch.BuildSA "
        "-d {input.fasta} "
        "-tda 0 "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "

# MSGFPlus
rule msgfplus:
    input:
        mzml = "mzml/{datafile}.mzML",
        fasta = 'work/database/target_decoy_database.fasta',
        index = 'work/database/target_decoy_database.canno'
    output:
        idxml = "work/msgfplus/{datafile}/dbsearch_{datafile}.idXML"
    singularity:
        config['singularity']['default']
    threads: 6
    priority: 10
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 16384
    benchmark:
        "work/msgfplus/{datafile}/dbsearch_{datafile}.benchmark.txt"
    params:
        pmt = "-precursor_mass_tolerance {0}".format(config["precursor"]["tolerance"]),
        pmu = "-precursor_error_units {0}".format(config["precursor"]["units"]),
        e = "-enzyme {0}".format(config["digestion"]["enzyme"]),
        fm = fm,
        vm = vm,
        inst = "-instrument {0}".format(config["msgfplus"]["inst"]),
        tryptic = msgfplus_tryptic,
        debug = '-debug {0}'.format(config["debug"]),
        log = 'work/msgfplus/{datafile}/dbsearch_{datafile}.log'
    shell:
        "MSGFPlusAdapter "
        "-in {input.mzml} -out {output.idxml} -database {input.fasta} "
        "-executable "
        # "/usr/local/openms_thirdparty/All/MSGFPlus/MSGFPlus.jar "
        "bin/msgfplus/MSGFPlus_20190418.jar "
        "-java_memory 16384 "
        "-isotope_error_range 0,0 "
        "-max_precursor_charge 3 "
        "-add_features true "
        "-max_mods 3 "
        "{params.pmt} "
        "{params.pmu} "
        "{params.e} "
        "{params.fm} "
        "{params.vm} "
        "{params.inst} "
        "{params.tryptic} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "
