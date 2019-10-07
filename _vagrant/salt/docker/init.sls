docker:
  pkg.installed:
    - pkgs:
      {% if grains['os_family'] == 'RedHat' %}
      - docker:
      {% elif grains['os_family'] == 'Debian' %}
      - docker.io
      {% endif %}
  user.present:
    - name: vagrant
  group.present:
    - system: True
    - addusers:
       - vagrant
  service.running:
    - enable: True