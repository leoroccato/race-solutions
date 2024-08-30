import xmltodict
import os
import time
import requests
import winsound

lista_arquivos = os.listdir(r"C:\TV\XML")
queimadas = []
informacoes = []


def calcular_segundos(tempo_str):
    partes = tempo_str.split(":")
    if len(partes) == 3:
        horas, minutos, segundos_milissegundos = partes
    elif len(partes) == 2:
        horas = "0"
        minutos, segundos_milissegundos = partes
    else:
        horas = "0"
        minutos = "0"
        segundos_milissegundos = partes[0]

    segundos_total = int(horas) * 3600  # Converta horas em segundos
    segundos_total += int(minutos) * 60  # Converta minutos em segundos
    segundos_total += float(segundos_milissegundos)  # Adicione os segundos e milissegundos
    return segundos_total


# Abrir o arquivo XML e pegar os dados de Evento e Pilotos
def pegar_infos_piloto(path_xml, stop_thread_velo, distancias, comboboxes, strings, limite):

    # Conjunto para armazenar identificadores únicos de entradas processadas
    processed_entries = set()

    while not stop_thread_velo.is_set():
        print('Running...')
        with open(path_xml, "rb") as file:
            time.sleep(1)
            xml_content = file.read()

        # Pegando Dados de Evento
        dic_arquivo = xmltodict.parse(xml_content)
        infos_pilotos = dic_arquivo["resultspage"]['results']

        if 'result' in infos_pilotos:
            pilotos_data = dic_arquivo['resultspage']['results'].get('result', [])
            for result in pilotos_data:
                for i in range(len(comboboxes)):
                    setor_selecionado = comboboxes[i]
                    string_usuario = strings[i]

                    # Verificar se a distância é válida
                    try:
                        distancia_usuario = float(distancias[i])
                    except (ValueError, TypeError):
                        continue

                    # Inicializa a variável de tempo como None
                    tempo = None

                    # Buscar o tempo correspondente ao setor selecionado no XML
                    if setor_selecionado == "Setor 3":
                        tempo = result.get('@section3')
                    elif setor_selecionado == "Setor 4":
                        tempo = result.get('@section4')
                    elif setor_selecionado == "Setor 5":
                        tempo = result.get('@section5')
                    elif setor_selecionado == "Setor 6":
                        tempo = result.get('@section6')
                    else:
                        continue  # Se o setor não corresponder, pula para a próxima entrada

                    # Verifica se o tempo é válido
                    if tempo and tempo != '':
                        try:
                            # Use a função calcular_segundos para converter o tempo
                            tempo_segundos = calcular_segundos(tempo)
                            velocidade_ms = distancia_usuario / tempo_segundos
                            velocidade_km = round(velocidade_ms * 3.6, 4)
                            print(velocidade_km)
                        except ValueError:
                            print(f"Erro ao converter tempo para segundos: {tempo}")
                            continue

                        # Cria um identificador único para a entrada
                        entry_id = (setor_selecionado, tempo)

                        # Verifica se a entrada já foi processada
                        if entry_id not in processed_entries:
                            # Se a velocidade for maior que 50 km/h, imprime a string do usuário
                            if velocidade_km > 50:
                                sessao = result.get('@runname')
                                lastline = result.get('@lasttimeline')
                                last_time_piloto = result.get('@lasttimeofday')
                                piloto = result.get('@firstname')
                                numero = result.get('@no')
                                winsound.Beep(534, 900)
                                informacoes.append({
                                    'trecho': "TIPO",
                                    'numero': numero,
                                    'piloto': piloto,
                                    'velocidade': velocidade_km,
                                })
                                # Envia os dados para o servidor Flask gerar o HTML
                                data = {
                                    'informacoes': informacoes
                                }
                                print(f"Enviando solicitação POST para o servidor Flask com dados: {data}")
                                response = requests.post('http://127.0.0.1:5000/atualizar_velocidade', json=data)
                                print(f"Status da resposta: {response.status_code}")
                                if response.status_code == 200:
                                    print('HTML generated successfully')
                                else:
                                    print(
                                        f'Failed to generate HTML: {response.status_code}, Response: {response.text}')
                                print(
                                    f'#{numero} {string_usuario} EM {velocidade_km} km/h - {sessao} - {last_time_piloto}')
                        else:
                            print(f"Tempo não encontrado ou inválido para o setor: {setor_selecionado}")
        time.sleep(1)  # Pequena pausa para evitar sobrecarga de processamento
    else:
        print("Não encontrei a chave 'results' no XML")


