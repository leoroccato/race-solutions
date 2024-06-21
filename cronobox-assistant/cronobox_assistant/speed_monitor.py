import xml.etree.ElementTree as ET
import xmltodict
import os
import winsound
from datetime import datetime
import time
from collections import defaultdict
import requests


lista_arquivos = os.listdir(r"C:\TV\XML")
queimadas = []
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


# Abrir o arquivo XML e pegar os dados de Evento e Pilotos
def pegar_infos_piloto(path_xml, stop_thread_velo):
    while not stop_thread_velo.is_set():
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
                setor6 = 0 if result.get('@section6') == '' else result.get('@section6')
                setor3 = 0 if result.get('@section3') == '' else result.get('@section3')
                setor5 = 0 if result.get('@section5') == '' else result.get('@section5')
                pit_time = 0 if result.get('@additional7') == '' else result.get('@additional7')
                last_time_piloto = result.get('@lasttimeofday')
                piloto = result.get('@firstname')
                tempo_pit_in = float(setor3)
                tempo_pit_out = float(setor5)
                tempo_total_segundos = 0
                pit_time_segundos = 0
                if setor6 != 0:
                    # Divida o tempo de pit em minutos, segundos e milissegundos
                    setor6_str = str(setor6)
                    tempo_total_segundos = calcular_segundos(setor6_str)
                if pit_time != 0:
                    pit_time_str = str(pit_time)
                    pit_time_segundos = calcular_segundos(pit_time_str)
                # Definindo velocidade de Entrada de Box
                print(lastline)
                if lastline == 'Pit In' and tempo_pit_in > 0:
                    velocidade_ms = 64.5 / tempo_pit_in
                    velocidade_km = round(velocidade_ms * 3.6, 4)
                    sessao = result.get('@runname')
                    if velocidade_km > 50 and velocidade_km not in queimadas:
                        print(f'QUEIMOU ENTRADA DE PIT {velocidade_km} KM/H')
                        velocidade_estouro = round(velocidade_km, 2)
                        queimadas.append(velocidade_km)
                        tipo = 'ENTRADA DE BOX'
                        informacoes.append({
                            'trecho': tipo,
                            'numero': numero,
                            'piloto': piloto,
                            'velocidade': velocidade_estouro,
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
                        print(f'#{numero} PENALIZADO POR QUEIMA DE VELOCIDADE DE {tipo} EM {velocidade_estouro} km/h - {sessao} - {last_time_piloto}')
                # Definindo velocidade de Pit Time
                elif lastline == 'Pit Out' and tempo_total_segundos > 0:
                    velocidade_ms = 346 / tempo_total_segundos
                    velocidade_km = round(velocidade_ms * 3.6, 4)
                    numero = result.get('@no')
                    sessao = result.get('@runname')
                    if velocidade_km > 45 and velocidade_km not in queimadas:
                        print(f'QUEIMOU PIT TIME {velocidade_km} KM/H')
                        velocidade_estouro = round(velocidade_km, 2)
                        queimadas.append(velocidade_km)
                        tipo = 'PIT TIME'
                        informacoes.append({
                            'trecho': tipo,
                            'numero': numero,
                            'piloto': piloto,
                            'velocidade': velocidade_estouro,
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
                        print(f'#{numero} PENALIZADO POR QUEIMA DE VELOCIDADE DE {tipo} EM {velocidade_estouro} km/h - {sessao} - {last_time_piloto}')
                    """if pit_time_segundos > 0:
                        pit_time_minimo = pit_time_segundos - 15
                        if tempo_total_segundos > pit_time_segundos and setor6_str not in pit_times:
                            flag = 'Cumpriu'
                            informacoes.append({
                                'trecho': flag,
                                'numero': numero,
                                'piloto': piloto,
                                'velocidade': velocidade_estouro,
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
                                informacoes.append({
                                    'trecho': flag,
                                    'numero': numero,
                                    'piloto': piloto,
                                    'velocidade': velocidade_estouro,
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
                                pit_times.append(setor6_str)
                            else:
                                flag = 'Não cumpriu'
                                informacoes.append({
                                    'trecho': flag,
                                    'numero': numero,
                                    'piloto': piloto,
                                    'velocidade': velocidade_estouro,
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
                                pit_times.append(setor6_str)"""
                # Definindo velocidade de Saída de Box
                elif lastline == 'Speed Pit Out' and tempo_pit_out > 0:
                    velocidade_ms = 245 / tempo_pit_out
                    velocidade_km = round(velocidade_ms * 3.6, 4)
                    numero = result.get('@no')
                    sessao = result.get('@runname')
                    if velocidade_km > 50 and velocidade_km not in queimadas:
                        print(f'QUEIMOU PIT TIME {velocidade_km} KM/H')
                        velocidade_estouro = round(velocidade_km, 2)
                        queimadas.append(velocidade_km)
                        tipo = 'SAÍDA DE BOX'
                        informacoes.append({
                            'trecho': tipo,
                            'numero': numero,
                            'piloto': piloto,
                            'velocidade': velocidade_estouro,
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
                        print(f'#{numero} PENALIZADO POR QUEIMA DE VELOCIDADE DE {tipo} EM {velocidade_estouro} km/h - {sessao} - {last_time_piloto}')
                else:
                    continue
        else:
            print("Não encontrei a chave 'results' no XML")


