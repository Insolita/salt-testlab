#!/bin/bash
DOCKER_PATH='_docker/'
SUITE_PATH="${PWD}/local_suites"
IMAGE='debian_stretch'
SUITE='demo'
HIGHSTATE='n'
VERBOSE='n'

if [[ ${#@} -lt 2 ]]; then
    usage
    exit 1
fi

for i in "$@"
do
case $i in
    -i=*|--image=*)
    IMAGE="${i#*=}"
    shift
    ;;
    -s=*|--suite=*)
    SUITE="${i#*=}"
    shift
    ;;
    --hs)
    HIGHSTATE='y'
    shift
    ;;
    --v)
    VERBOSE='y'
    shift
    ;;
    *)
    ;;
esac
done

usage(){
    echo "Usage:"
    echo " -i(--image)= required, docker image name"
    echo " -s(--suite)= required, suite name"
    echo " --hs optional flag, execute highstate"
    echo " --v optional flag, verbose mode"
    echo "EXAMPLE: ./run_docker.sh -i=debian_stretch -s=demo --hs "
}

info() {
    if [[ $VERBOSE == 'y' ]]; then
       printf "*  INFO: %s\n" "$@";
    fi
}
error() {
    printf "* ERROR: %s\n" "$@" 1>&2;
}



if  docker ps | grep -q ${IMAGE} ; then
    info "Remove previous container"
    docker rm -f ${IMAGE}
fi

 

docker build -t ${IMAGE} ${DOCKER_PATH}${IMAGE} > /dev/null
info "docker ${IMAGE} compiled"
docker run --name ${IMAGE} --privileged -d -v ${SUITE_PATH}/${SUITE}:/srv/salt ${IMAGE} tail -f /dev/null
info "docker ${IMAGE} runned"
if [[ $HIGHSTATE == 'y' ]]; then
   docker exec -ti ${IMAGE} sh -c 'cd /srv/salt && salt-call --local state.highstate'
else
  info "docker runned, use it as"
  echo ":> docker exec -ti ${IMAGE} /bin/bash "   
  exit 0
fi