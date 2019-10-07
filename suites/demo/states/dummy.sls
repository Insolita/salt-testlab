show_foo_pillar:
    cmd.run:
       - name: 'echo {{pillar.get('foo')}}'

{% for b in pillar.get('bar') %}
show_bar_{{b}}_pillar_item:
    cmd.run:
       - name: 'echo {{b}}'       
{% endfor %}

{% for baz in pillar.get('baz') %}
show_bar_{{baz.name}}_pillar_item:
    cmd.run:
       - name: 'echo {{baz.name}}: x={{baz.x}} y={{baz.y}}'       
{% endfor %}