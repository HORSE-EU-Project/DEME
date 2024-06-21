#!/bin/bash
MINOR_VERSION=$1
PORT=8091
SCRIPT_DIR=$(dirname $(readlink -f "$0"))

function start_container() {
TARGET=/home/app
echo "start_container"
docker run \
    --rm -it \
    --mount type=bind,source="$SCRIPT_DIR",target=$TARGET \
    -p $PORT:$PORT \
    -e PORT=$PORT \
    deme-mockup-engine:0.1.0-${MINOR_VERSION}
}

main() {
    if [ -z "$MINOR_VERSION" ]; then
        echo "Usage: ./run-deme-mockup <MINOR_VERSION>"
        exit 1
    fi

    start_container
}

main
exit 0
