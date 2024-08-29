from jinja2 import Environment, FileSystemLoader


def gerar_pagina_html(informacoes, template_name, horario_safety_car=None):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    if horario_safety_car is not None:
        return template.render(informacoes=informacoes, horario_safety_car=horario_safety_car)
    else:
        return template.render(informacoes=informacoes)
