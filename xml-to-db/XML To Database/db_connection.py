import psycopg2


def database_connect():
    try:
        conn = psycopg2.connect(
            database="Cronobox_DB",
            host="localhost",
            user="postgres",
            password="cancer09",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar no banco de dados: {e}")
        return None


def database_insert_evento(conn, etapa, bandeira, grupo, melhor_volta_por, melhor_volta, voltas, voltas_para_fim,
                           cronometro, nome_evento, tipo_corrida, hora_do_dia, regressivo):
    try:
        cur = conn.cursor()

        sql = """INSERT INTO dados_xml_evento (
                            etapa, bandeira, grupo, melhor_volta_por, melhor_volta, voltas,
                            voltas_para_fim, cronometro, nome_evento, tipo_corrida, hora_do_dia, regressivo
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        data = (etapa, bandeira, grupo, melhor_volta_por, melhor_volta, voltas, voltas_para_fim, cronometro,
                nome_evento, tipo_corrida, hora_do_dia, regressivo)
        cur.execute(sql, data)

        conn.commit()

        cur.close()
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")


def database_insert_piloto(conn,
                                melhorsetor3, melhorsetor2, melhorsetor1, setor3, setor2, setor1, timeline, tempododia,
                                pitstops, melhornavolta, melhorvolta, intervalo, diferenca, tempototal, ultimavolta,
                                abreviado, contagemmanual, piloto2, piloto1, bop, categoria, equipe, firstname, numero,
                           posicaonacategoria, posicao, marcador, ultimapassagem, ultimotempo, tempoideal,
                           patchcarroslocal, patchcarros, patchcategoria, voltaspiloto1, voltaspiloto2, voltaspiloto3,
                           tempoidealdiferenca, evento
                           ):
    try:
        cur = conn.cursor()

        sql = """INSERT INTO dados_xml_corridas (
                            melhorsetor3, melhorsetor2, melhorsetor1, setor3, setor2, setor1, timeline, tempododia,
                            pitstops, melhornavolta, melhorvolta, intervalo, diferenca, tempototal, ultimavolta,
                            abreviado, contagemmanual, piloto2, piloto1, bop, categoria, equipe, firstname, numero,
                            posicaonacategoria, posicao, marcador, ultimapassagem, ultimotempo, tempoideal,
                            patchcarroslocal, patchcarros, patchcategoria, voltaspiloto1, voltaspiloto2, voltaspiloto3,
                            tempoidealdiferenca, evento
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (
            melhorsetor3, melhorsetor2, melhorsetor1, setor3, setor2, setor1, timeline, tempododia,
                               pitstops, melhornavolta, melhorvolta, intervalo, diferenca, tempototal, ultimavolta,
                               abreviado, contagemmanual, piloto2, piloto1, bop, categoria, equipe, firstname, numero,
                                posicaonacategoria, posicao, marcador, ultimapassagem, ultimotempo, tempoideal,
                            patchcarroslocal, patchcarros, patchcategoria, voltaspiloto1, voltaspiloto2, voltaspiloto3,
                             tempoidealdiferenca, evento
        )
        cur.execute(sql, data)

        conn.commit()

        cur.close()
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")


def database(tipo_insert, etapa=None, bandeira=None, grupo=None, melhor_volta_por=None, melhor_volta=None, voltas=None,
             voltas_para_fim=None, cronometro=None, nome_evento=None, tipo_corrida=None, hora_do_dia=None, regressivo=None,
             melhorsetor3=None, melhorsetor2=None, melhorsetor1=None, setor3=None, setor2=None, setor1=None,
             timeline=None, tempododia=None, pitstops=None, melhornavolta=None, melhorvolta=None, intervalo=None,
             diferenca=None, tempototal=None, ultimavolta=None, abreviado=None, contagemmanual=None, piloto2=None,
             piloto1=None, bop=None, categoria=None, equipe=None, firstname=None, numero=None, posicaonacategoria=None,
             posicao=None, marcador=None, ultimapassagem=None, ultimotempo=None, tempoideal=None, patchcarroslocal=None,
             patchcarros=None, patchcategoria=None, voltaspiloto1=None, voltaspiloto2=None, voltaspiloto3=None,
             tempoidealdiferenca=None, evento=None):
    conn = database_connect()

    if tipo_insert == 'evento' and conn:
        database_insert_evento(conn, etapa, bandeira, grupo, melhor_volta_por, melhor_volta, voltas, voltas_para_fim,
                               cronometro, nome_evento, tipo_corrida, hora_do_dia, regressivo)

        conn.close()

    if tipo_insert == 'piloto' and conn:
        database_insert_piloto(conn,
                                melhorsetor3, melhorsetor2, melhorsetor1, setor3, setor2, setor1, timeline, tempododia,
                                pitstops, melhornavolta, melhorvolta, intervalo, diferenca, tempototal, ultimavolta,
                                abreviado, contagemmanual, piloto2, piloto1, bop, categoria, equipe, firstname, numero,
                               posicaonacategoria, posicao, marcador, ultimapassagem, ultimotempo, tempoideal,
                                patchcarroslocal, patchcarros, patchcategoria, voltaspiloto1, voltaspiloto2, voltaspiloto3,
                               tempoidealdiferenca, evento)
        conn.close()




