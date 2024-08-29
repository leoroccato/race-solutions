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
def pegar_infos_piloto(path_xml, stop_thread_velo, pitin, timein, pitout, limite):
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
                if setor6 != 0:
                    # Divida o tempo de pit em minutos, segundos e milissegundos
                    setor6_str = str(setor6)
                    tempo_total_segundos = calcular_segundos(setor6_str)
                if pit_time != 0:
                    pit_time_str = str(pit_time)
                # Definindo velocidade de Entrada de Box
                if lastline == 'Speed Pit Out':
                    print(lastline, tempo_pit_out)
                # QUEIMA DE VELOCIDADE DE ENTRADA DE BOX
                if lastline == 'Pit In' and tempo_pit_in > 0:
                    velocidade_ms = float(pitin) / tempo_pit_in
                    velocidade_km = round(velocidade_ms * 3.6, 4)
                    sessao = result.get('@runname')
                    if velocidade_km > float(limite) and velocidade_km not in queimadas:
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
                # QUEIMA DE VELOCIDADE DE PIT TIME
                elif lastline == 'Pit Out' and tempo_total_segundos > 0:
                    print('meio')
                    print(timein)
                    velocidade_ms = float(timein) / tempo_total_segundos
                    velocidade_km = round(velocidade_ms * 3.6, 4)
                    numero = result.get('@no')
                    sessao = result.get('@runname')
                    if velocidade_km > float(limite) and velocidade_km not in queimadas:
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
                # QUEIMA DE VELOCIDADE DE SAIDA DE BOX
                elif lastline == 'Speed Pit Out' and tempo_pit_out > 0:
                    print('saida')
                    print(pitout)
                    velocidade_ms = float(pitout) / tempo_pit_out
                    velocidade_km = round(velocidade_ms * 3.6, 4)
                    numero = result.get('@no')
                    print('Cheguei aqui')
                    print(velocidade_km)
                    if velocidade_km > float(limite) and velocidade_km not in queimadas:
                        print(f'QUEIMOU PIT TIME {velocidade_km} KM/H')
                        velocidade_estouro = round(velocidade_km, 2)
                        queimadas.append(velocidade_km)
                        tipo = 'SAÍDA DE BOX'
                        classe = 'highlight'
                        winsound.Beep(534, 900)
                        informacoes.append({
                            'trecho': tipo,
                            'numero': numero,
                            'piloto': piloto,
                            'velocidade': velocidade_estouro,
                            'classe': classe
                        })
                        # Envia os dados para o servidor Flask gerar o HTML
                        data = {
                            'informacoes': informacoes
                        }
                        requests.post('http://127.0.0.1:5000/atualizar_velocidade', json=data)
                else:
                    continue
        else:
            print("Não encontrei a chave 'results' no XML")


