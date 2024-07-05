#!/usr/bin/bash

#absolute_path=$(cd $(dirname "$0") && pwd)
absolute_path=$(dirname $(readlink -f "${BASH_SOURCE[0]}"))
export NVIDEOS_MODULE_NAME="nvideos_web"
export NVIDEOS_SRC="nvideos_web"
export NVIDEOS_PATH="${absolute_path}"

wnvideos.runlocal(){
    python3 -m "$NVIDEOS_MODULE_NAME"
}
wnvideos.export_env_vars(){
    set -o allexport
    source "${NVIDEOS_PATH}/.env.webserver"
    set +o allexport
}
wnvideos.start_postgres(){
    sudo bash -c "docker compose up postgres -d"
}
wnvideos.kill_any_pg_and_up_nvideo_pg(){
    PG_DB_CONTAINER_NAME="nvideos_postgres"
    PG_DB_PORT="5432"

    isRunning=false

    containers=$(sudo docker ps --format "{{.ID}} {{.Names}} {{.Ports}}")s
    while IFS= read -r line; do
        #echo $line
        
        # Splitting the return from docker ps
        # IFS - Internal Field Separator
        IFS=' ' read -r -a array <<< $line
        containerId=${array[0]}
        nameContainer=${array[1]}
        ports=${array[2]}

        if [[ "$PG_DB_CONTAINER_NAME" == "$nameContainer" ]]; then
            isRunning=true
        fi

        if 
        [[ "$PG_DB_CONTAINER_NAME" != "$nameContainer" ]] && 
        [[ "$ports" == *"$PG_DB_PORT"* ]]; 
        then
            sudo docker kill "$containerId"
        fi

        if [[ $isRunning == false ]]; then
            sudo docker compose up postgres -d
        fi

    done <<< $containers
}

# Validations
wnvideos.mypy(){
    python3 -m mypy "$NVIDEOS_PATH/$NVIDEOS_SRC"
}
wnvideos.unit_tests(){
    python3 "$NVIDEOS_PATH/$NVIDEOS_SRC/tests/main_tests.py" $1
}