#!/bin/bash

set -e

SCRIPT=`basename "$0"`
if [ ! $# == 1 ]; then
    printf "\n $SCRIPT script needs a parameter: test, scan, or purge. \n ex: '$SCRIPT test' \n\n"
    exit 1
fi

OPTION=$1
NETWORK="ci_net"
CYAN='\033[1;36m'
PURPLE='\033[1;35m'
NC='\033[0m'

function ci {
  case $OPTION in
    test) build
          uat
    ;;
    scan) image_scan
    ;;
    purge) purge_containers
    ;;
    *) printf "\n *** Selection $OPTION not found, exiting. ***\n\n"
          exit 1
  esac
}

function build {
  echo -e "${CYAN}---- Building docker image ----${NC}"

  docker build -t local/poc_app .
  
  echo -e "${PURPLE}---- Build complete ----${NC}"
}

function uat {
  PULL_IMAGES=(tutum/curl)
  pull_images
  echo -e "${CYAN}---- Start UAT tests ----${NC}"

  docker network create $NETWORK || true
  docker run -d --net $NETWORK --name poc-app local/poc_app
  docker run --rm -i \
    -v $PWD:/tmp \
    -w /tmp/tests \
    --net $NETWORK \
    tutum/curl bash -C uat.sh poc-app
  docker tag local/poc_app christiantragesser/poc_app

  echo -e "${PURPLE}---- Testing complete ----${NC}"
}

function image_scan {
  PULL_IMAGES=(arminc/clair-db:latest ubuntu arminc/clair-local-scan:v2.0.1 christiantragesser/clair-scanner)
  pull_images
  echo -e "${CYAN}---- Docker image CVE scan ----${NC}"
 
  docker network create $NETWORK || true
  docker run -d --name postgres --net $NETWORK arminc/clair-db:latest
  docker run --rm --net $NETWORK ubuntu bash -c "while ! timeout 1 bash -c 'cat < /dev/null > /dev/tcp/postgres/5432' &>/dev/null; do :; done"
  docker run -d --name clair --net $NETWORK arminc/clair-local-scan:v2.0.1
  docker run --rm -i --net $NETWORK \
    -v $PWD:/tmp \
    -v /var/run/docker.sock:/var/run/docker.sock \
    christiantragesser/clair-scanner sh -c "/opt/clair-scan.sh christiantragesser/poc_app"

  echo -e "${PURPLE}---- CVE scan complete ----${NC}"
}

function pull_images {
  for IMAGE in ${PULL_IMAGES[@]};
  do
    echo -e "${CYAN}+ Pulling image ${IMAGE}:${NC}"
    docker pull $IMAGE;
  done  
}

function purge_containers {
  echo -e "${CYAN}---- CI docker container clean up ----${NC}"

  docker rm -f poc-app postgres clair || true
  docker network rm $NETWORK || true

  echo -e "${PURPLE}---- clean up complete ----${NC}"
}

ci