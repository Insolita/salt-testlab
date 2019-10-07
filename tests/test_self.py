"""
Self-test.
Test the configuration of our own salt-dev machine. The salt-dev box is Ubuntu.
"""

import pytest
import testinfra
from conftest import salt_call

HOST_ID = "salt-dev"

@pytest.fixture(scope='module', params=['ubuntu_bionic', 'debian_stretch'])
def image_name(request):
    """
    Override conftest default
    """
    yield request.param
 
def test_docker_installed(host):
    file = host.file("/usr/bin/docker")
    assert file.exists

def test_docker_running(host):
    file = host.file("/var/run/docker.sock")
    assert file.exists
    assert file.group == "docker"

def test_salt_installed(host):
    file = host.file("/etc/salt/minion")
    assert file.exists

def test_provision(host, docker_host, image_name):
    assert host.docker(image_name).name == image_name
    assert host.docker(image_name).is_running
    #assert host.package('python3-pip').is_installed
    #assert host.service('salt-minion').is_running
    assert docker_host.package('python3').is_installed
    assert docker_host.service('ssh').is_enabled
    
    #print(host.salt('grains.item', 'os'))
    #print(docker_host.salt('grains.item', 'os'))
    #print(docker_host.salt('state.show_sls', 'in_docker', local = True))
    salt_call(docker_host, '--id=%s state.highstate' % image_name)
    assert docker_host.package('cowsay').is_installed
    print(docker_host.pip_package.get_packages(pip_path='pip3'))



