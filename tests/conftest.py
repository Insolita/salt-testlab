import pytest
import testinfra
import subprocess
from os import path

containers = ['debian_stretch', 'debian_buster', 'ubuntu_bionic']
local = testinfra.get_host('local://')

def base_path(append = ''):
    basepath = path.dirname(path.dirname(__file__))
    if len(append):
        return path.join(basepath, append)
    return basepath

def dockers_dir():
    return base_path('_docker')

def pytest_addoption(parser):
    parser.addoption("--image", action="store", help="docker-image name")

@pytest.fixture(scope='module', params=containers)
def image_name(request):
    '''
      Override this function in custom modules for run custom images
    '''
    yield request.param

@pytest.fixture(scope='module')
def volume_map():
    """
    This fixture returns the volume map between source salt states path and docker 
    Override this fixture in your module if you need map another states directories
    @example
       return ['/srv/suites/xxx:/srv/salt']
    """        

    return ['%s:/srv/salt' % base_path('salt')]

    
@pytest.fixture(scope='module', autouse=True)
def docker_host(request, image_name, volume_map):
    image_path = '%s/%s' % (dockers_dir(), image_name)
    print('docker image_path ', image_path)
    # build images
    cmd = local.run("docker build -t %s %s" % (image_name, image_path))
    assert cmd.rc == 0
    volumes = ' '.join(['-v %s' % v for v in volume_map])
    print(volumes)
    # run a container
    docker_id = local.check_output(
        "docker run --name %s --privileged -d %s %s tail -f /dev/null" % (image_name, volumes, image_name)
        )
    print(' Run ', image_name, ' id=', docker_id)
    def teardown():
        print("\nteardown docker ", docker_id)
        local.run("docker rm -f %s", docker_id)

    request.addfinalizer(teardown)
    # return a testinfra connection to the container
    docker = testinfra.get_host("docker://" + docker_id)
    yield docker