from flask import Flask, render_template, request, jsonify
from generate_html import gerar_pagina_html

app = Flask(__name__)

# Armazena as informações globais
informacoes_globais = []
informacoes_velocidade = []
horario_safety_car_global = ""

# ------------------------ ROTAS PÁGINAS HTML


@app.route('/pagina_safety')
def index():
    return render_template('index_safety.html')


@app.route('/pagina_velocidade')
def pagina_velocidade():
    return render_template('index_velocidade.html')

# ------------------------ MÉTODOS GET


@app.route('/dados_horario', methods=['GET'])
def dados_horario():
    global horario_safety_car_global
    horario_safety_car = horario_safety_car_global if horario_safety_car_global else '--'
    return jsonify({
        'horario_safety_car': horario_safety_car
    })


@app.route('/dados_pilotos', methods=['GET'])
def dados_pilotos():
    global informacoes_globais
    return jsonify({
        'informacoes': informacoes_globais
    })


@app.route('/dados_velocidade', methods=['GET'])
def dados_velocidade():
    return jsonify({
        'informacoes': informacoes_velocidade
    })

# ------------------------ MÉTODOS POST


@app.route('/atualizar_horario', methods=['POST'])
def atualizar_horario():
    template_name = 'index_safety.html'
    global horario_safety_car_global
    print("Recebendo solicitação POST em /atualizar_horario")
    try:
        horario_safety_car = request.json.get('horario_safety_car')
        if horario_safety_car is None:
            raise ValueError("horario_safety_car não fornecido")

        # Atualiza o horario_safety_car_global
        horario_safety_car_global = horario_safety_car

        # Gera o HTML atualizado
        html_content = gerar_pagina_html(informacoes_globais, template_name, horario_safety_car_global)

        # Salva o HTML atualizado no arquivo
        with open('templates/index_safety.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        return 'Horário do safety car atualizado com sucesso', 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/atualizar_pilotos', methods=['POST'])
def atualizar_pilotos():
    template_name = 'index_safety.html'
    global informacoes_globais
    print("Recebendo solicitação POST em /atualizar_pilotos")
    try:
        informacoes = request.json.get('informacoes')
        if informacoes is None:
            raise ValueError("informacoes não fornecido")

        # Atualiza as informações globais
        informacoes_globais = informacoes

        # Gera o HTML atualizado
        html_content = gerar_pagina_html(informacoes_globais, template_name, horario_safety_car_global)

        # Salva o HTML atualizado no arquivo
        with open('templates/index_safety.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        return 'Informações dos pilotos atualizadas com sucesso', 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/atualizar_velocidade', methods=['POST'])
def atualizar_velocidade():
    template_name = 'index_velocidade.html'
    global informacoes_velocidade
    print("Recebendo solicitação POST em /atualizar_velocidade")
    try:
        informacoes = request.json.get('informacoes')
        if informacoes is None:
            raise ValueError("informacoes não fornecido")

        # Atualiza as informações globais
        informacoes_velocidade = informacoes

        # Gera o HTML atualizado
        html_content = gerar_pagina_html(informacoes_velocidade, template_name)

        # Salva o HTML atualizado no arquivo
        with open('templates/index_velocidade.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        return 'Informações de velocidade atualizadas com sucesso', 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500
"""
@app.route('/atualizar_pitstops', methods=['POST'])
def atualizar_velocidade():
    template_name = 'index_pitstop.html'
    global informacoes_velocidade
    print("Recebendo solicitação POST em /atualizar_velocidade")
    try:
        informacoes = request.json.get('informacoes')
        if informacoes is None:
            raise ValueError("informacoes não fornecido")

        # Atualiza as informações globais
        informacoes_velocidade = informacoes

        # Gera o HTML atualizado
        html_content = gerar_pagina_html(informacoes_velocidade, template_name)

        # Salva o HTML atualizado no arquivo
        with open('templates/index_pitstop.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        return 'Informações de velocidade atualizadas com sucesso', 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500
"""

@app.route('/reset_dados', methods=['POST'])
def reset_dados():
    global informacoes_globais, horario_safety_car_global
    print("Recebendo solicitação POST em /reset_dados")
    try:
        # Limpa os dados globais
        informacoes_globais = []
        horario_safety_car_global = ""
        return 'Dados resetados com sucesso', 200
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


def run_server():
    app.run(debug=True, port=5000, use_reloader=False, threaded=True)


if __name__ == '__main__':
    run_server()
