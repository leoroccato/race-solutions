import xml.etree.ElementTree as ET
import requests
import time


def meteorologia():
    # Credenciais de Usuário
    application_key = '5ADB6B1771BF3EE37B9E407402F717A9'
    api_key = 'c77c431f-4dab-4c17-8f1d-fa99308e5902'
    mac_code = '94:3C:C6:45:2B:A7'

    # Chamada da API
    url = f'https://api.ecowitt.net/api/v3/device/real_time?application_key={application_key}&api_key={api_key}&mac={mac_code}&call_back=all'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if not data['data']:
            print()
            print("Não há dados, verifique se a estação está ligada!")
            print()
        else:
            print("-----------------------------------------------------")
            print("Conectado a Estação com Sucesso!")
            ground_temperature = data["data"]["outdoor"]["temperature"]["value"]
            ambient_temperature = data["data"]["indoor"]["temperature"]["value"]
            humidity = data["data"]["outdoor"]["humidity"]["value"]
            wind_speed = data["data"]["wind"]["wind_speed"]["value"]
            wind_direction = data["data"]["wind"]["wind_direction"]["value"]
            pressure = data["data"]["pressure"]["absolute"]["value"]

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

            # Criando a estrutura XML para export
            live_data = {
                "ambient_temperature": ambient_temperature_converted,
                "ground_temperature": ground_temperature_converted,
                "humidity": humidity,
                "wind_speed": wind_speed_converted,
                "wind_direction": wind_direction_index,
                "pressure": pressure_converted
            }

            root = ET.Element("live_data")

            for name, data in live_data.items():
                entry = ET.SubElement(root, "data")
                entry.set("name", name)
                entry.text = str(data)

            tree = ET.ElementTree(root)

            tree.write(r"C:\TV\XML\Extras\meteorologia.xml")

            print(f"Arquivo XML gerado! Nova medição em 5 minutos...\n"
                  f"Temperatura Ambiente: {ambient_temperature_converted} C\n"
                  f"Temperatura da Pista: {ground_temperature_converted} C\n"
                  f"Umidade: {humidity} %\n"
                  f"Velocidade do Vento: {wind_speed_converted} km/h\n"
                  f"Direção do Vento: {wind_direction_index}\n"
                  f"Pressão Atmosférica: {pressure_converted} hPa\n")
            print("Para finalizar o programa digite Ctrl + C")
            print("-----------------------------------------------------")
    else:
        print('Erro na requisição da API: ', response.status_code)


# Loop para executar a funcao a cada 5 minutos
while True:
    meteorologia()
    time.sleep(5 * 60)
