# File Conversion:
rule convert_raw_files:
    input:
        raw = expand("{location}/{{datafile}}.raw",location=config["raw"]["location"]),
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
        "wine msconvert "
        "{input.raw} "
        "--mzML "
        "-o mzml "
        "--outfile {wildcards.datafile}.mzML "
        "--filter \"peakPicking true 1-\" "
        "--filter \"zeroSamples removeExtra\" "
        "2>&1 | tee {params.log} "
