#!/bin/bash
git pull

# Get the latest git commit hash
tag_name=$(git rev-parse --short HEAD)
data_folder=$(pwd)/../data
log_folder=$(pwd)/logging
config_folder=$(pwd)/config
docker_name="energie-api${tag_name}"

PS3='Build for (Ocean Server/Raspberry Server)?: '
server_options=("Ocean Server" "Raspberry Server")
select server in "${server_options[@]}"
do
    case $server in
        "Ocean Server")
            dockerfile="Dockerfile"
            image_name="python:3.11.0-slim-buster"
            break
            ;;
        "Raspberry Server")
            dockerfile="Dockerraspfile"
            image_name="python:3.11-slim-bookworm"
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

PS3='Build What?: '
# options=("dev" "acc" "prod" "Quit")
options=("dev" "prod" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "dev")
            echo "Building for DEV"
            port="5001:5000"
            break
            ;;
        "prod")
            echo "Building for PROD"
            port="5001:5000"
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

docker build -f "$dockerfile" -t "$docker_name" .

docker run -it -d --restart on-failure:3 -p "$port" -v "$data_folder:/src/data" -v "$log_folder:/src/logging" -v "$config_folder:/src/config" -e "TZ=Europe/Amsterdam" --log-opt tag="$docker_name/$image_name" --name="$docker_name" "$docker_name"

docker ps -a
