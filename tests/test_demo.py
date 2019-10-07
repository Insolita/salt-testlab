"""
Self-test.
Test the configuration of our own salt-dev machine. The salt-dev box is Ubuntu.
"""

import pytest
import subprocess
import testinfra
from conftest import base_path


@pytest.fixture(scope='module')
def volume_map():
    """
    Override conftest default
    """
    return ['%s:/srv/salt' % base_path('suites/demo')]    

def test_highstate(host, docker_host, image_name):
    assert host.docker(image_name).is_running
    pillars = docker_host.salt('pillar.ls', [], local = True)
    assert len(pillars) == 3
    print(pillars)
    assert docker_host.salt('pillar.get', 'foo', local = True) == 'bar'
    #print(docker_host.salt('state.show_sls', 'states.dummy', local = True))
    print(docker_host.salt('state.highstate', image_name, local = True))



