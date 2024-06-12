import xmltodict
import os
import db_connection

lista_arquivos = os.listdir(r"C:\TV\XML")
path_xml = r"C:\TV\XML\current.xml"


# Abrir o arquivo XML e pegar os dados de Evento e Pilotos
def pegar_infos(path_xml):
    with open(path_xml, "rb") as file:
        xml_content = file.read()
    # Pegando Dados de Evento
    dic_arquivo = xmltodict.parse(xml_content)

    #print(json.dumps(dic_arquivo, indent=4))
    infos_evento = dic_arquivo["resultspage"]['label']
    #print(json.dumps(infos_evento, indent=4))
    infos_pilotos = dic_arquivo["resultspage"]['results']

    dic_evento = {}
    dic_pilotos = {}
    lista_pilotos = []

    # Coletar dados de Evento
    for info in infos_evento:
        if "@type" in info and "#text" in info:
            tipo = info["@type"]
            texto = info["#text"]

            if tipo == "bestlapby":
                melhor_volta_por = texto
                dic_evento[tipo] = texto
            elif tipo == "bestlaptime":
                melhor_volta = texto
                dic_evento[tipo] = texto
            elif tipo == "eventname":
                etapa = texto
                dic_evento[tipo] = texto
            elif tipo == "flag":
                bandeira = texto
                dic_evento[tipo] = texto
            elif tipo == "groupname":
                grupo = texto
                dic_evento[tipo] = texto
            elif tipo == "laps":
                if texto == "":
                    voltas = 0
                    dic_evento[tipo] = texto
                else:
                    voltas = texto
                    dic_evento[tipo] = texto
            elif tipo == "lapstogo":
                if texto == "":
                    voltas_para_fim = 0
                    dic_evento[tipo] = texto
                else:
                    voltas_para_fim = texto
                    dic_evento[tipo] = texto
            elif tipo == "racetime":
                if texto == "":
                    cronometro = "00:00"
                    dic_evento[tipo] = texto
                else:
                    cronometro = texto
                    dic_evento[tipo] = texto
            elif tipo == "runname":
                nome_evento = texto
                dic_evento[tipo] = texto
            elif tipo == "runtype":
                tipo_corrida = texto
                dic_evento[tipo] = texto
            elif tipo == "timeofday":
                hora_do_dia = texto
                dic_evento[tipo] = texto
            elif tipo == "timetogo":
                regressivo = texto
                dic_evento[tipo] = texto
        else:
            if "@type" in info:
                tipo = info["@type"]
                if tipo == "lapstogo":
                    voltas_para_fim = 0
                if tipo == "timetogo":
                    regressivo = ""
    tipo_insert = 'evento'
    db_connection.database(tipo_insert, etapa, bandeira, grupo, melhor_volta_por, melhor_volta, voltas, voltas_para_fim, cronometro,
                           nome_evento, tipo_corrida, hora_do_dia, regressivo)
    print('Subi no banco dados de evento')

    # Contar a quantidade de Pilotos na corrida
    if 'result' in infos_pilotos:
        results_data = dic_arquivo['resultspage']['results'].get('result', [])
        if isinstance(results_data, list):
            qtd_pilotos = len(results_data)
            print(f"Quantidade de Pilotos: {qtd_pilotos}")
            # Coletar os dados dos Pilotos

            for result in results_data:
                dic_pilotos = {
                    'melhorsetor3': None if result.get('@bestsection3') == '' else result.get('@bestsection3'),
                    'melhorsetor2': None if result.get('@bestsection2') == '' else result.get('@bestsection2'),
                    'melhorsetor1': None if result.get('@bestsection1') == '' else result.get('@bestsection1'),
                    'setor3': None if result.get('@section2') == '' else result.get('@section2'),
                    'setor2': None if result.get('@section1') == '' else result.get('@section1'),
                    'setor1': None if result.get('@section0') == '' else result.get('@section0'),
                    'timeline': 'PIT IN' if result.get('@lasttimeline').lower() == 'pit in' else ('PIT OUT' if result.get('@lasttimeline').lower == 'pit out' else result.get('@lasttimeline').upper()),
                    'tempododia': result.get('@lasttimeofday'),
                    'pitstops': '0' if result.get('@nopitstops') == '' else result.get('@nopitstops'),
                    'melhornavolta': result.get('@bestinlap'), # Não adicionei a verificação se é 0
                    'melhorvolta': None if result.get('@besttime') == '' else result.get('@besttime'),
                    'intervalo': None if result.get('@difference') == '' else result.get('@difference'),
                    'diferenca': result.get('@gap'),
                    'tempototal': result.get('@totaltime'),
                    'ultimavolta': 'PIT IN' if result.get('@lasttime').lower() == 'in pit' else ('PIT OUT' if result.get('@lasttime').lower == 'out' else result.get('@lasttime')),
                    'voltas': result.get('@laps'), # Não adicionei a verificacao se é vazio
                    'abreviado': result.get('@additional8'),
                    'contagemmanual': result.get('@additional6'),
                    'piloto2': result.get('@additional4'),
                    'piloto1': result.get('@additional2'),
                    'bop': None if result.get('@additional1') == '' else result.get('@additional1'),
                    'categoria': result.get('@class'),
                    'equipe': result.get('@fullname'),
                    'firstname': result.get('@firstname'),
                    'numero': result.get('@no'),
                    'posicaonacategoria': result.get('@positioninclass'),
                    'posicao': result.get('@position'),
                    'marcador': result.get('@marker'),
                    'ultimapassagem': result.get('@lasttimeofday'),
                    'ultimotempo': result.get('@lasttime'),
                    'tempoideal': None,
                    'patchcarroslocal': None,
                    'patchcarros': None,
                    'patchcategoria': None,
                    'voltaspiloto1': 0,
                    'voltaspiloto2': 0,
                    'voltaspiloto3': 0,
                    'tempoidealdiferenca': '0',
                }
                lista_pilotos.append(dic_pilotos)
                tipo_insert = 'piloto'
                db_connection.database(
                    tipo_insert,
                    **dic_pilotos
                )
                print('Subi no banco dados de volta')
    else:
        print("Não encontrei a chave 'results' no XML")


while True:
    pegar_infos(path_xml)




