#!/usr/bin/env bash

#abort on error
set -e

function usage
{
    echo "usage: run_pipeline -d -s SOME_MORE_ARGS [-y YET_MORE_ARGS || -h]"
    echo "   ";
    echo "  -d | --debug             : do a dry_run";
    echo "  -s | --shell             : open docker shell";
    echo "  -m | --memory            : pipeline memory";
    echo "  -c | --cores             : pipeline cores";
    echo "  -h | --help              : This message";
}

function parse_args
{
  # positional args
  args=()

  # named args
  while [ "$1" != "" ]; do
      case "$1" in
          -d | --debug )    debug="--dryrun";             ;;
          -s | --shell )    shell=1;                      ;;
          -m | --memory )   mem="--resources mem_mb=$2";  shift;;
          -c | --cores )    cores="--cores $2";           shift;;
          -h | --help )     usage;                        exit;; # quit and show usage
          * )               args+=("$1")             # if no match, add it to the positional args
      esac
      shift # move to next kv pair
  done

  # restore positional args
  set -- "${args[@]}"

  # # set positionals to vars
  # positional_1="${args[0]}"
  # positional_2="${args[1]}"

  # # validate required args
  # if [[ -z "${debug}" || -z "${some_more_args}" ]]; then
  #     echo "Invalid arguments"
  #     usage
  #     exit;
  # fi

  # # set defaults
  # if [[ -z "$yet_more_args" ]]; then 
  #     yet_more_args="a default value";
  # fi
}


function run
{
  parse_args "$@"

  rnd_id=$RANDOM

  #docker login registry.gitlab.com -u mfreitas -p aoeLHVW7XvyQ9VfjxHWm

  # docker_image=openms240
  # docker_version=latest
  docker_image=austinu17/proteomic_workflow
  docker_version=run_1
  data=${PWD}

  echo "Starting up OpenMS Docker"
  echo "version $docker_mm_ver"
  echo Starting up $docker_image:$docker_version

  if [[ "$(docker images -q $docker_image:$docker_version 2> /dev/null)" == "" ]]; then
    echo "Image not found. Pulling from dockerhub"
    docker pull $docker_image:$docker_version
  fi

  if [[ $shell == 1 ]]; then
    docker run --rm -it \
          -v "$data":"/data" \
        --name pipeline_worker_$rnd_id \
        $docker_image:$docker_version \
        /bin/bash 
  else
    docker run --rm -it \
          -v "$data":"/data" \
        --name pipeline_worker_$rnd_id \
        $docker_image:$docker_version \
        /bin/bash -c "cd /data  && snakemake --snakefile Snakefile.py --unlock && snakemake --snakefile Snakefile.py -p --keep-going $cores $mem $debug"
  fi 
}

run "$@";
