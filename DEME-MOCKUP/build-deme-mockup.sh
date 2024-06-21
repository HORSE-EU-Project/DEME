#!/bin/bash
MINOR_VERSION=$1
[[ -z "$MINOR_VERSION" ]] && echo "need minor version" && exit 1

docker build . -t deme-mockup-engine:0.1.0-${MINOR_VERSION}
