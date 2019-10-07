include:
  - python.pip

docker-py:
  pip.installed:
    - bin_env: /usr/bin/pip3
    - require:
      - sls: python.pip