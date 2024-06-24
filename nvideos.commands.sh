#!/usr/bin/bash

absolute_path=$(pwd)
export NVIDEOS_PATH="${absolute_path}"

wnvideos.runlocal(){
    python3 -m nvideos_web
}
wnvideos.export_env_vars(){
    set -o allexport
    source "${NVIDEOS_PATH}/.env.webserver"
    set +o allexport
}
wnvideos.start_postgres(){
    sudo bash -c "docker compose up postgres -d"
}