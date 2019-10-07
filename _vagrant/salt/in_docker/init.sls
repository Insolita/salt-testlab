include:
  - python.pip

cowsay:
    pkg.installed

figlet:
    pkg.installed

cherrypy:
    pip.installed:
      - bin_env: /usr/bin/pip3
      - require:
          - sls: python.pip
