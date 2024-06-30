import time
import xmltodict
import os
import requests
from collections import defaultdict

lista_arquivos = os.listdir(r"C:\TV\XML")
pit_times = []
car_pits = []
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


def verificar_pit(car_pits):
    contagem = defaultdict(int)

    for numero in car_pits:
        contagem[numero] += 1

        if contagem[numero] == 3:
            return numero
    return None


def pitstop_monitor(path_xml, stop_thread_pitstop):
    while not stop_thread_pitstop.is_set():
        print('Running...')
        with open(path_xml, "rb") as file:
            time.sleep(1)
            xml_content = file.read()

        # Pegando Dados de Evento
        dic_arquivo = xmltodict.parse(xml_content)

        # print(json.dumps(infos_evento, indent=4))
        infos_pilotos = dic_arquivo["resultspage"]['results']
        if 'result' in infos_pilotos:
            pilotos_data = dic_arquivo['resultspage']['results'].get('result', [])
            for result in pilotos_data:
                lastline = result.get('@lasttimeline')
                numero = result.get('@no')
                piloto = result.get('@firstname')
                setor6 = 0 if result.get('@section6') == '' else result.get('@section6')
                pit_time = 0 if result.get('@additional7') == '' else result.get('@additional7')
                pit_time_segundos = 0
                if pit_time != 0:
                    pit_time_str = str(pit_time)
                    pit_time_segundos = verificar_pit(pit_time_str)
                if setor6 != 0:
                    # Divida o tempo de pit em minutos, segundos e milissegundos
                    setor6_str = str(setor6)
                    tempo_total_segundos = calcular_segundos(setor6_str)
                if lastline == 'Pit Out' and pit_time_segundos > 0:
                    if pit_time_segundos > 0:
                        pit_time_minimo = pit_time_segundos - 15
                        if tempo_total_segundos > pit_time_segundos and setor6_str not in pit_times:
                            flag = 'Cumpriu'
                            classe_linha = 'hightlight'
                            informacoes.append({
                                'numero': flag,
                                'piloto': numero,
                                'pitstop': piloto,
                                'tempo': tempo_total_segundos,
                                'classe': classe_linha
                            })
                            # Envia os dados para o servidor Flask gerar o HTML
                            data = {
                                'informacoes': informacoes
                            }

                            print(f"Enviando solicitação POST para o servidor Flask com dados: {data}")

                            response = requests.post('http://127.0.0.1:5000/atualizar_pitstop', json=data)
                            print(f"Status da resposta: {response.status_code}")
                            if response.status_code == 200:
                                print('HTML generated successfully')

                            else:
                                print(
                                    f'Failed to generate HTML: {response.status_code}, Response: {response.text}')
                            car_pits.append(numero)
                            pit_times.append(setor6_str)

                            numero_repetido = verificar_pit(car_pits)

                            if numero_repetido is not None:
                                print(f"#{numero_repetido} JÁ CUMPRIU AS 3 PARADAS OBRIGATÓRIAS")
                                print(car_pits)
                            else:
                                print("Nenhum número se repete três vezes na lista.")
                        elif tempo_total_segundos < pit_time_segundos and setor6_str not in pit_times:
                            if tempo_total_segundos > pit_time_minimo:
                                flag = 'Penalização'
                                classe_linha = 'hightlight'
                                informacoes.append({
                                    'numero': flag,
                                    'piloto': numero,
                                    'pitstop': piloto,
                                    'tempo': tempo_total_segundos,
                                    'classe': classe_linha
                                })
                                # Envia os dados para o servidor Flask gerar o HTML
                                data = {
                                    'informacoes': informacoes
                                }

                                print(f"Enviando solicitação POST para o servidor Flask com dados: {data}")

                                response = requests.post('http://127.0.0.1:5000/atualizar_pitstop', json=data)
                                print(f"Status da resposta: {response.status_code}")
                                if response.status_code == 200:
                                    print('HTML generated successfully')

                                else:
                                    print(
                                        f'Failed to generate HTML: {response.status_code}, Response: {response.text}')
                                pit_times.append(setor6_str)
                            else:
                                flag = 'Não cumpriu'
                                classe_linha = 'hightlight'
                                informacoes.append({
                                    'numero': flag,
                                    'piloto': numero,
                                    'pitstop': piloto,
                                    'tempo': tempo_total_segundos,
                                    'classe': classe_linha
                                })
                                # Envia os dados para o servidor Flask gerar o HTML
                                data = {
                                    'informacoes': informacoes
                                }

                                print(f"Enviando solicitação POST para o servidor Flask com dados: {data}")

                                response = requests.post('http://127.0.0.1:5000/atualizar_pitstop', json=data)
                                print(f"Status da resposta: {response.status_code}")
                                if response.status_code == 200:
                                    print('HTML generated successfully')
                                else:
                                    print(
                                        f'Failed to generate HTML: {response.status_code}, Response: {response.text}')
                                pit_times.append(setor6_str)