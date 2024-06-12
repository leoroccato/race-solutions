from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import matplotlib.pyplot as plt
import xmltodict
import requests
import traceback
import logging
import pytz
import time
import sys
import os

# Configurando o logger
log_path = r'C:\TV\Meteorologia\log.txt'
logging.basicConfig(filename=log_path, level=logging.ERROR)

# Cria as listas

# Listas Temporárias
temperaturas_ambiente_temp = []
temperaturas_pista_temp = []
umidades_temp = []
velocidades_vento_temp = []
direcoes_vento_temp = []
pressoes_temp = []
precipitacao_temp = []

# Lista Fixa
temperaturas_ambiente = []
temperaturas_pista = []
umidades = []
velocidades_vento = []
direcoes_vento = []
pressoes = []
precipitacao = []

path_xml = r"C:\TV\XML\current.xml"
#path_xml = r"C:\Users\leoro\Desktop\Projetos\Cronometragem\Python\pythonCronobox\Cronobox\current.xml" Debug


def log_error(error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"{timestamp} - {error_message}\n")


def meteorologia():

    # Credenciais de Usuário
    application_key = '5ADB6B1771BF3EE37B9E407402F717A9'
    api_key = 'c77c431f-4dab-4c17-8f1d-fa99308e5902'
    mac_code = '94:3C:C6:45:2B:A7'

    # Horário
    horario_atual = datetime.now()
    # Formatando o horário para o padrão desejado (por exemplo, "HH:MM:SS")
    horario_formatado = horario_atual.strftime("%H:%M:%S")

    # Chamada da API
    url = f'https://api.ecowitt.net/api/v3/device/real_time?application_key={application_key}&api_key={api_key}&mac={mac_code}&call_back=all'
    #url = f'http://localhost:3000/start' Debug

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if not data['data']:
            print()
            print("Não há dados, verifique se a estação está ligada!")
            print()
        else:
            ground_temperature = data["data"]["outdoor"]["temperature"]["value"]
            ambient_temperature = data["data"]["indoor"]["temperature"]["value"]
            humidity = data["data"]["outdoor"]["humidity"]["value"]
            wind_speed = data["data"]["wind"]["wind_speed"]["value"]
            wind_direction = data["data"]["wind"]["wind_direction"]["value"]
            pressure = data["data"]["pressure"]["absolute"]["value"]
            rain_rate = data["data"]["rainfall_piezo"]["rain_rate"]["value"]

            # Conversões

            # Ambient Fahrenheit -> Celsius
            ambient_temperature = float(ambient_temperature)
            ambient_temperature_converted = round((ambient_temperature - 32) * 5.0 / 9.0, 1)

            # Ground Fahrenheit -> Celsius
            ground_temperature = float(ground_temperature)
            ground_temperature_converted = round(((ground_temperature - 32) * 5.0 / 9.0), 1)

            # Mph -> Kmh
            wind_speed = float(wind_speed)
            wind_speed_converted = round(wind_speed * 1.60934, 1)

            # Direcoes
            wind_direction = float(wind_direction)
            direcoes = ['N', 'NE', 'L', 'SE', 'S', 'SO', 'O', 'NO']
            wind_direction_calc = int(wind_direction / (360 / len(direcoes))) % len(direcoes)
            wind_direction_index = direcoes[wind_direction_calc]

            # Pressao
            pressure = float(pressure)
            pressure_converted = round(pressure * 33.8639, 0)

            # Precipitação
            rain_rate = float(rain_rate)
            rain_rate_converted = round(rain_rate * 25.4, 1)

            # Salvar nas listas temporárias
            temperaturas_ambiente_temp.append(ambient_temperature_converted)
            temperaturas_pista_temp.append(ground_temperature_converted)
            umidades_temp.append(humidity)
            velocidades_vento_temp.append(wind_speed_converted)
            direcoes_vento_temp.append(wind_direction_index)
            pressoes_temp.append(pressure_converted)
            precipitacao_temp.append(rain_rate_converted)

            # Salvar nas listas fixas
            temperaturas_ambiente.append(ambient_temperature_converted)
            temperaturas_pista.append(ground_temperature_converted)
            umidades.append(humidity)
            velocidades_vento.append(wind_speed_converted)
            direcoes_vento.append(wind_direction_index)
            pressoes.append(pressure_converted)
            precipitacao.append(rain_rate_converted)
    else:
        print('Erro na requisição da API: ', response.status_code)


def gerar_relatorio_graficos(path_header, groupname, runname, hora_inicial_execucao):

    # Criar pasta para salvar relatório
    data = datetime.now()
    data_format = data.strftime('%Y-%m-%d')
    path = f"C:/TV/Meteorologia/{groupname} - {data_format}"
    if not os.path.exists(path):
        os.makedirs(path)

    name_arquivo = f'{groupname} - {runname} - MTE GRAFICOS.pdf'
    caminho_arquivo = os.path.join(path, name_arquivo)

    # Criar o documento PDF
    c = canvas.Canvas(caminho_arquivo, pagesize=letter)

    # Adicionar a imagem de cabeçalho
    altura_pagina = 792
    largura_pagina = 612

    c.drawImage(path_header, 50, altura_pagina - 100, width=largura_pagina - 350, height=65)

    # Adicionar título
    titulo_evento = f"{groupname} - {runname}"
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(largura_pagina / 2, altura_pagina - 130, titulo_evento)

    # Gerar os gráficos
    graficos = [
        (temperaturas_ambiente_temp, "Temperatura Ambiente"),
        (temperaturas_pista_temp, "Temperatura da Pista"),
        (pressoes_temp, "Pressão Atmosférica"),
        (umidades_temp, "Umidade"),
        (velocidades_vento_temp, "Velocidade do Vento"),
        (direcoes_vento_temp, "Direção do Vento")
    ]

    labels = [
        "(°C)",
        "(°C)",
        "(hPa)",
        "(%)",
        "(km/h)",
        "Direção"
    ]

    # Configurando intervalos de tempo de leitura
    hora_final_execucao = datetime.now(pytz.timezone('America/Sao_Paulo')).replace(second=0, microsecond=0)
    horarios = [hora_inicial_execucao]
    while horarios[-1] < hora_final_execucao:

        horarios.append(horarios[-1] + timedelta(minutes=3))

    if horarios[-1] > hora_final_execucao:
        horarios.pop()
    horarios_formatados = [hora.strftime('%H:%M') for hora in horarios]

    fig, axs = plt.subplots(3, 2, figsize=(10, 8))

    coluna_atual = 0

    # Criando os gráficos
    for (dados, titulo), labels, ax in zip(graficos, labels, axs.flatten()):

        if coluna_atual == 2:
            coluna_atual = 0  # Resetar contador

        ax.plot(range(len(dados)), dados, color='black')
        marcadores_x = [0, len(dados) - 1]
        marcadores_y = [dados[0], dados[-1]]
        ax.plot(marcadores_x, marcadores_y, 'ro')
        ax.set_xticks(marcadores_x)
        ax.set_xticklabels([horarios_formatados[0], horarios_formatados[-1]])
        ax.set_title(f'{titulo}', fontweight='bold')
        ax.set_ylabel(f'{labels}', fontweight='bold')
        ax.grid(axis='y')

        coluna_atual += 1

    plt.tight_layout()

    plt.savefig(r'C:\TV\graficos.png')

    graficos_path = r'C:\TV\graficos.png'

    c.drawImage(graficos_path, 50, altura_pagina - 650, width=largura_pagina - 100, height=altura_pagina - 300)

    c.save()
    return horarios_formatados


def gerar_relatorio_completo(path_header, groupname, runname, horarios_formatados):

    # Criar pasta para salvar relatório
    data = datetime.now()
    data_format = data.strftime('%Y-%m-%d')
    path = f"C:/TV/Meteorologia/{groupname} - {data_format}"
    if not os.path.exists(path):
        os.makedirs(path)

    name_arquivo = f'{groupname} - {runname} - MTE COMPLETO.pdf'
    caminho_arquivo = os.path.join(path, name_arquivo)

    # Criar documento PDF
    doc = SimpleDocTemplate(caminho_arquivo, pagesize=letter, leftMargin=35, rightMargin=0, topMargin=30, bottomMargin=0)

    # Adicionar elementos ao PDF
    elements = []

    # Adicionar imagem do PDF
    imagem = Image(path_header, width=262, height=65)
    imagem.hAlign = 'LEFT'
    elements.append(imagem)

    # Adicionar título
    titulo = f"{groupname} - {runname}"
    style_titulo = ParagraphStyle(
        name='Titulo',
        fontName='Helvetica-Bold',
        fontSize=16,
        alignment=TA_CENTER,
    )
    titulo_paragrafo = Paragraph(titulo, style_titulo)
    elements.append(Spacer(1, 25))
    elements.append(titulo_paragrafo)

    # Criar lista de dados meteorológicos
    dados_meteorologicos = [
        ['Hora', 'Temp. Amb. (°C)', 'Temp. Pista (ºC)', 'Umid. (%)', 'Pressão (hPa)',
         'Vento (m/s)', 'Direção', 'Precip. (mm/hr)'],
    ]

    # Estilo da tabela
    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Cor de fundo preta para o cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Cor do texto branco para o cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento central para todas as células
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte em negrito para o cabeçalho
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Cor de fundo branca para o conteúdo da tabela
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Borda preta para todas as células
    ])

    # Adicionar os valores das colunas às linhas da tabela, alternando as cores de fundo
    cor_fundo = [colors.white, colors.lightgrey]
    estilos_linhas = []
    for i, (hora, temp_a, temp_p, umid, press, vento, direcoes, precip) \
            in enumerate(zip(horarios_formatados, temperaturas_ambiente_temp, temperaturas_pista_temp, umidades_temp,
                             pressoes_temp, velocidades_vento_temp, direcoes_vento_temp, precipitacao_temp)):
        dados_meteorologicos.append([hora, temp_a, temp_p, umid, press, vento, direcoes, precip])
        cor_atual = cor_fundo[i % len(cor_fundo)]
        estilo_linha = ('BACKGROUND', (0, i + 1), (-1, i + 1), cor_atual)
        estilos_linhas.append(estilo_linha)

    # Criar tabela com os dados meteorológicos
    tabela = Table(dados_meteorologicos)

    # Aplicar estilo à tabela para cada linha
    for estilo_linha in estilos_linhas:
        tabela.setStyle(TableStyle([estilo_linha]))

    # Aplicar estilo adicional à tabela (cabeçalho)
    estilo_cabecalho = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]
    tabela.setStyle(TableStyle(estilo_cabecalho))

    # Adiciona aos elementos
    elements.append(Spacer(1, 25))
    elements.append(tabela)

    # Cria o documento
    doc.build(elements)


def gerar_relatorio_diario(path_header, groupname, hora_inicial_execucao_dia, hora_final_execucao):

    # Obter a data de hoje
    data = datetime.now()
    data_format = data.strftime('%Y-%m-%d')
    data_hoje = data.strftime("%d/%m/%Y")

    # Horarios do Documento
    horarios = [hora_inicial_execucao_dia]
    while horarios[-1] < hora_final_execucao:
        horarios.append(horarios[-1] + timedelta(minutes=5))

    horarios_dia = [hora.strftime('%H:%M') for hora in horarios]

    # Criar documento PDF
    doc = SimpleDocTemplate(f"C:/TV/Meteorologia/{groupname} - {data_format}/Relatorio_Diario_{groupname}_{data_format}.pdf", pagesize=letter, leftMargin=35,
                            rightMargin=0, topMargin=30, bottomMargin=0)

    # Adicionar elementos ao PDF
    elements = []

    # Adicionar imagem do PDF
    imagem = Image(path_header, width=262, height=65)
    imagem.hAlign = 'LEFT'
    elements.append(imagem)

    # Adicionar título
    titulo = f"Relatório Diário {data_hoje}"
    style_titulo = ParagraphStyle(
        name='Titulo',
        fontName='Helvetica-Bold',
        fontSize=16,
        alignment=TA_CENTER,
    )
    titulo_paragrafo = Paragraph(titulo, style_titulo)
    elements.append(Spacer(1, 25))
    elements.append(titulo_paragrafo)

    # Criar lista de dados meteorológicos
    dados_meteorologicos = [
        ['Hora', 'Temp. Amb. (°C)', 'Temp. Pista (ºC)', 'Umid. (%)', 'Pressão (hPa)',
         'Vento (m/s)', 'Direção', 'Precip. (mm/hr)'],
    ]

    # Estilo da tabela
    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Cor de fundo preta para o cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Cor do texto branco para o cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento central para todas as células
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte em negrito para o cabeçalho
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Cor de fundo branca para o conteúdo da tabela
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Borda preta para todas as células
    ])

    # Adicionar os valores das colunas às linhas da tabela, alternando as cores de fundo
    cor_fundo = [colors.white, colors.lightgrey]
    estilos_linhas = []
    for i, (hora, temp_a, temp_p, umid, press, vento, direcoes, precip) \
            in enumerate(zip(horarios_dia, temperaturas_ambiente, temperaturas_pista, umidades,
                             pressoes, velocidades_vento, direcoes_vento, precipitacao)):
        dados_meteorologicos.append([hora, temp_a, temp_p, umid, press, vento, direcoes, precip])
        cor_atual = cor_fundo[i % len(cor_fundo)]
        estilo_linha = ('BACKGROUND', (0, i + 1), (-1, i + 1), cor_atual)
        estilos_linhas.append(estilo_linha)

    # Criar tabela com os dados meteorológicos
    tabela = Table(dados_meteorologicos)

    # Aplicar estilo à tabela para cada linha
    for estilo_linha in estilos_linhas:
        tabela.setStyle(TableStyle([estilo_linha]))

    # Aplicar estilo adicional à tabela (cabeçalho)
    estilo_cabecalho = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]
    tabela.setStyle(TableStyle(estilo_cabecalho))

    # Adiciona aos elementos
    elements.append(Spacer(1, 25))
    elements.append(tabela)

    # Cria o documento
    doc.build(elements)


def leitura_xml(path_xml):

    # Ler current.xml
    with open(path_xml, "rb") as file:
        xml_content = file.read()

    # Pegando Dados de Evento
    dic_arquivo = xmltodict.parse(xml_content)
    infos_evento = dic_arquivo["resultspage"]['label']

    # Coletar Nome da Corrida e Bandeira Atual
    for info in infos_evento:
        if "@type" in info and "#text" in info:
            tipo = info["@type"]
            texto = info["#text"]
            if tipo == "flag":
                flag = texto
            elif tipo == "runname":
                runname = texto
            elif tipo == "groupname":
                groupname = texto
    return flag, runname, groupname


def gerar_relatorio(path_header, groupname, runname, hora_inicial_execucao):
    try:
        print('Corrida encerrada, gerando relatório...')
        horarios_formatados = gerar_relatorio_graficos(path_header, groupname, runname, hora_inicial_execucao)
        gerar_relatorio_completo(path_header, groupname, runname, horarios_formatados)
        print(f'Relatório gerado, {groupname} - {runname}, aguardando nova alteração da bandeira...')
    except Exception as e:
        print(f'Erro ao encerrar o programa: {e}')


def encerrar_programa(path_header, groupname, hora_inicial_execucao_dia):
    try:
        print('Encerrando programa e gerando relatório diário...')
        hora_final_execucao = datetime.now(pytz.timezone('America/Sao_Paulo')).replace(second=0, microsecond=0)
        gerar_relatorio_diario(path_header, groupname, hora_inicial_execucao_dia, hora_final_execucao)
        print('Programa encerrado.')
    except Exception as e:
        print(f'Erro ao encerrar o programa: {e}')
    finally:
        sys.exit()  # Encerrar o programa após a geração do relatório diário


def esperar_verificar(runname, groupname):
    tempo_total = 3 * 60
    intervalo = 1
    contador = 0
    # Verificar se a bandeira foi alterada antes do reinicio do contador
    while contador < tempo_total:
        old_runname = None
        old_groupname = None
        runname_check = leitura_xml(path_xml)[1]
        # Caso tenha sido alterada, retornar da função o nome antigo da sessão
        if runname_check != runname:
            print(f'{runname_check} = {runname}')
            old_runname = runname
            old_groupname = groupname
            break
        else:
            time.sleep(intervalo)
            contador += intervalo
    return old_runname, old_groupname


def main():
    # Perguntar ao usuário o caminho da imagem do Header
    while True:
        try:
            path_header = input("Insira o caminho da imagem que irá no cabeçalho do Relatório: ")
            with open(path_header, 'rb') as file:
                pass
            break
        except FileNotFoundError:
            print("Caminho inválido. Por favor, insira um caminho válido.")
        except Exception as e:
            print("O caminho inserido é inválido, por favor insira um caminho válido:", e)
    print()
    print(f"Aguardando alteração da Bandeira para iniciar leitura... Certifique-se que o XML está sendo exportado para {path_xml}")
    print()

    # Rotina de Execução do Programa
    bandeira_inicial = None

    # Setando a hora de inicio da execução
    hora_inicial_execucao = datetime.now(pytz.timezone('America/Sao_Paulo')).replace(second=0, microsecond=0)
    hora_inicial_execucao_dia = datetime.now(pytz.timezone('America/Sao_Paulo')).replace(second=0, microsecond=0)

    # Rotina de execução do programa
    try:
        while True:
            try:
                flag, runname, groupname = leitura_xml(path_xml)
                if bandeira_inicial is None:            # Verifica se a bandeira ainda não foi definida ou foi resetada
                    if flag not in ['none', 'warmup']:  # Verifica se a bandeira é verde
                        print('Bandeira alterada, iniciando leitura...')
                        bandeira_inicial = flag
                else:
                    if flag in ['none', 'warmup']:      # Verifica se a bandeira é None ou Warmup
                        print('Corrida encerrada, gerando relatório...')
                        print('---------------------------------------------------------------------------------------')
                        if old_runname != runname and old_runname is not None:
                            horarios_formatados = gerar_relatorio_graficos(path_header, old_groupname, old_runname, hora_inicial_execucao)
                            gerar_relatorio_completo(path_header, old_groupname, old_runname, horarios_formatados)
                            print(f'Relatório gerado: {old_groupname} - {old_runname}. Aguardando nova alteração da bandeira...')
                            old_runname = None
                            old_groupname = None
                        elif old_runname is None:
                            horarios_formatados = gerar_relatorio_graficos(path_header, groupname, runname, hora_inicial_execucao)
                            gerar_relatorio_completo(path_header, groupname, runname, horarios_formatados)
                            print(f'Relatório gerado: {groupname} - {runname}. Aguardando nova alteração da bandeira...')
                        bandeira_inicial = None
                        hora_inicial_execucao = datetime.now(pytz.timezone('America/Sao_Paulo')).replace(second=0, microsecond=0)
                if flag not in ['none', 'warmup']:      # Verifica se a bandeira é verde
                    meteorologia()
                    old_runname, old_groupname = esperar_verificar(runname, groupname)
            except Exception as e:
                error_message = f"An exception occurred: {str(e)}\n{traceback.format_exc()}"
                log_error(error_message)
    except KeyboardInterrupt:
        encerrar_programa(path_header, groupname, hora_inicial_execucao_dia)


if __name__ == "__main__":
    main()