base:
  'salt-dev':
    - docker
    - testinfra

  'debian_*':
    - in_docker

  'ubuntu_*':
    - in_docker