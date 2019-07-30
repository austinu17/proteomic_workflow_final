#!/usr/bin/env bash

name="ds_notebook_extra"

echo "Stopping DS Notebook"
docker container stop $name
docker rm $name
