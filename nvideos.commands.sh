#!/usr/bin/bash

absolute_path=$(pwd)
export NVIDEOS_PATH="${absolute_path}"

wnvideos_runlocal(){
    python3 "${NVIDEOS_PATH}/nvideos_web/main.py"
}
wnvideos_export_env_vars(){
    set -o allexport
    source "${NVIDEOS_PATH}/nvideos_web/.env"
    set +o allexport
}