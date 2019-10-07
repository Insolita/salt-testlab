include:
  - python.pip

testinfra:
  pip.installed:
    - bin_env: /usr/bin/pip3
    - require:
      - sls: python.pip