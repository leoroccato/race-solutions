from jinja2 import Environment, FileSystemLoader


def gerar_pagina_html(informacoes, template_name, horario_safety_car=None):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    if horario_safety_car is not None:
        return template.render(informacoes=informacoes, horario_safety_car=horario_safety_car)
    else:
        return template.render(informacoes=informacoes)


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de informações processadas do XML
    informacoes = [
        {"horario_passagem": "1:24.356", "numero": "34", "piloto": "Lewis Hamilton", "categoria": "P1", "carro": "Ferrari"},
        # Adicione mais informações conforme necessário
    ]
    horario_safety_car = "1:22.356"
    gerar_pagina_html(informacoes, horario_safety_car)
