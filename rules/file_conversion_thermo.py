# File Conversion:
rule convert_thermo_files:
    input:
        raw = "raw/{datafile}.raw"
    output:
        mzml = temp("mzml/{datafile}.mzML.tmp")
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "mzml/{datafile}.benchmark.txt"
    priority: 1
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'mzml/{datafile}.log'
    shell:
        "mono "
        "bin/thermorawfileparser/ThermoRawFileParser_v117/ThermoRawFileParser.exe "
        "-i={input.raw} "
        "-b={output.mzml} "
        "-f=2 "
        #"-v "
        "2>&1 | tee {params.log} "

# File Conversion:
rule fix_mzml_files:
    input:
        mzml = "mzml/{datafile}.mzML.tmp"
    output:
        mzml = "mzml/{datafile}.mzML"
    singularity:
        config['singularity']['default']
    threads: 1
    resources:
        mem_mb=lambda wildcards, attempt: attempt * 8000
    benchmark:
        "mzml/{datafile}.benchmark.txt"
    priority: 1
    params:
        debug = '-debug {0}'.format(config["debug"]),
        log = 'mzml/{datafile}.log'
    shell:
        "FileConverter "
        "-in {input.mzml} "
        "-out {output.mzml} "
        "-threads {threads} "
        "{params.debug} "
        "2>&1 | tee {params.log} "
