# Padrão
from datetime import datetime
import time
import requests
# Terceiros
import xml.etree.ElementTree as ET
import xmltodict


# Listas
passagens = []
flags = []
pilotos = []


def main_loop(path_xml, stop_thread_safety):
    # Inicializa a variável da bandeira
    last_flag_value = None
    while not stop_thread_safety.is_set():
        # Pegando Dados de Evento do XML (Current)
        tree = ET.parse(path_xml)
        root = tree.getroot()

        # Encontra o node da flag
        flag = root.find(".//label[@type='flag']")
        if flag is not None and flag.text != last_flag_value:
            last_flag_value = flag.text
            print(f"Flag atualizada para: {last_flag_value}")

        # Rotina de capturar pit stops
        if last_flag_value != 'yellow':
            while last_flag_value != 'yellow':
                with open(path_xml, "rb") as file:
                    time.sleep(1)
                    xml_content = file.read()
                # Lê novamente o XML (Current)
                dic_arquivo = xmltodict.parse(xml_content)
                infos_pilotos = dic_arquivo['resultspage']['results']
                info_evento = dic_arquivo['resultspage']['label']
                # Atualiza o valor da flag novamente
                for info in info_evento:
                    if '@type' in info and info['@type'] == 'flag':
                        last_flag_value = info['#text']
                        break
                if 'result' in infos_pilotos:
                    pilotos_data = infos_pilotos.get('result', [])
                    for result in pilotos_data:
                        # Obtem valores da última linha, numero e último tempo do dia
                        lastline = result.get('@lasttimeline')
                        numero = result.get('@no')
                        last_time_piloto = result.get('@lasttimeofday')
                        carro = result.get('@additional3')
                        cat = result.get('@class')
                        piloto = result.get('@firstname')
                        if last_time_piloto:
                            last_time_piloto_formatted = datetime.strptime(last_time_piloto, "%H:%M:%S.%f").time()
                        if lastline == 'Pit In':
                            if last_time_piloto_formatted not in passagens:
                                if last_time_piloto_formatted not in passagens:
                                    classe_linha = 'normal'
                                    pilotos.append({
                                        'horario_passagem': last_time_piloto,
                                        'numero': numero,
                                        'piloto': piloto,
                                        'categoria': cat,
                                        'carro': carro,
                                        'classe': classe_linha
                                    })
                                    # Envia os dados para o servidor Flask gerar o HTML
                                    data = {
                                        'informacoes': pilotos
                                    }

                                    print(f"Enviando solicitação POST para o servidor Flask com dados: {data}")

                                    response = requests.post('http://127.0.0.1:5000/atualizar_pilotos', json=data)
                                    print(f"Status da resposta: {response.status_code}")
                                    if response.status_code == 200:
                                        print('HTML generated successfully')

                                    else:
                                        print(
                                            f'Failed to generate HTML: {response.status_code}, Response: {response.text}')
                                    passagens.append(last_time_piloto_formatted)
        # Rotina para caso a flag seja amarela
        if last_flag_value == 'yellow':
            # Salva o horário do dia
            flag_time = root.find(".//label[@type='timeofday']")
            flag_time = flag_time.text if flag_time is not None else "Unknown time"
            data = {
                'horario_safety_car': flag_time
            }

            print(f"Enviando solicitação POST para o servidor Flask com dados: {data}")

            response = requests.post('http://127.0.0.1:5000/atualizar_horario', json=data)
            print(f"Status da resposta: {response.status_code}")
            if response.status_code == 200:
                print('HTML generated successfully')

            else:
                print(
                    f'Failed to generate HTML: {response.status_code}, Response: {response.text}')
            if not flags:
                # Lista vazia
                flags.append(flag_time)
                print(f"Flag time: {flag_time}")
                # Rotina para executar durante a bandeira amarela
                while last_flag_value == 'yellow':
                    with open(path_xml, "rb") as file:
                        time.sleep(1)
                        xml_content = file.read()
                    # Lê novamente o XML (Current)
                    dic_arquivo = xmltodict.parse(xml_content)
                    infos_pilotos = dic_arquivo['resultspage']['results']
                    info_evento = dic_arquivo['resultspage']['label']
                    # Atualiza o valor da flag novamente
                    for info in info_evento:
                        if '@type' in info and info['@type'] == 'flag':
                            last_flag_value = info['#text']
                            break
                    if 'result' in infos_pilotos:
                        pilotos_data = infos_pilotos.get('result', [])
                        for result in pilotos_data:
                            # Obtem valores da última linha, numero e último tempo do dia
                            lastline = result.get('@lasttimeline')
                            numero = result.get('@no')
                            last_time_piloto = result.get('@lasttimeofday')
                            carro = result.get('@additional3')
                            cat = result.get('@class')
                            piloto = result.get('@firstname')
                            if last_time_piloto:
                                last_time_piloto_formatted = datetime.strptime(last_time_piloto, "%H:%M:%S.%f").time()
                            flag_time_formatted = datetime.strptime(flag_time, "%H:%M:%S").time()
                            # Comparar tempo do piloto com tempo da bandeira
                            if last_time_piloto_formatted > flag_time_formatted and lastline == 'Pit In':  # Safety Line
                                if last_time_piloto_formatted not in passagens:
                                    classe_linha = 'highlight'
                                    pilotos.append({
                                        'horario_passagem': last_time_piloto,
                                        'numero': numero,
                                        'piloto': piloto,
                                        'categoria': cat,
                                        'carro': carro,
                                        'classe': classe_linha
                                    })
                                    # Envia os dados para o servidor Flask gerar o HTML
                                    data = {
                                        'informacoes': pilotos
                                    }

                                    print(f"Enviando solicitação POST para o servidor Flask com dados: {data}")

                                    response = requests.post('http://127.0.0.1:5000/atualizar_pilotos', json=data)
                                    print(f"Status da resposta: {response.status_code}")
                                    if response.status_code == 200:
                                        print('HTML generated successfully')

                                    else:
                                        print(
                                            f'Failed to generate HTML: {response.status_code}, Response: {response.text}')
                                    passagens.append(last_time_piloto_formatted)
                    else:
                        print("Não encontrei a chave 'result' nos resultados do XML")
        time.sleep(1)  # Delay para evitar sobrecarga no loop
