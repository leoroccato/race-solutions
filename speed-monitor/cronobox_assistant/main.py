# Padrão
import webbrowser
import threading
import time
import requests
# Terceiros
import customtkinter as ctk
# Módulos
from server import run_server
from safety_car_monitor import main_loop
from speed_monitor import pegar_infos_piloto

# Flags de controle das threads de eventos
stop_thread_safety = threading.Event()
stop_thread_velo = threading.Event()
stop_thread_pitstop = threading.Event()

# ---------------------Funções Auxiliares------------------------------------


# Função para limpar a tela
def limpar_tela():
    try:
        response = requests.post('http://127.0.0.1:5000/reset_dados')
        if response.status_code == 200:
            print('Dados resetados com sucesso')
            # Chama a função JavaScript para limpar a tabela no navegador
            requests.post('http://127.0.0.1:5000/reset_frontend')
        else:
            print(f'Erro ao resetar dados: {response.status_code}, {response.text}')
    except Exception as e:
        print(f'Erro ao conectar ao servidor para resetar dados: {e}')


# Função para iniciar o servidor
def iniciar_server():
    # Iniciar o servidor Flask em uma thread separada
    threading.Thread(target=run_server).start()

# ---------------------Safety Controls------------------------------------


# Função para iniciar o programa do Safety
def iniciar_programa_safety():
    if entrada.get() == '':
        path_xml = r'C:\TV\XML\current.xml'
    else:
        path_xml = entrada.get()
    stop_thread_safety.clear()
    limpar_tela()
    # Abrir o navegador na página do Safety
    time.sleep(1)  # Delay para garantir que o servidor esteja pronto
    webbrowser.open('http://127.0.0.1:5000/pagina_safety')
    threading.Thread(target=main_loop, args=(path_xml, stop_thread_safety)).start()


# Função para reiniciar o programa do Safety
def reiniciar_programa_safety():
    stop_thread_safety.set()
    time.sleep(2)
    stop_thread_safety.clear()
    if entrada.get() == '':
        path_xml = r'C:\TV\XML\current.xml'
    else:
        path_xml = entrada.get()
    limpar_tela()
    threading.Thread(target=main_loop, args=(path_xml, stop_thread_safety)).start()


# Função para finalizar o programa do Safety
def finalizar_programa_safety():
    limpar_tela()
    stop_thread_safety.set()

# ---------------------Velocidade Controls------------------------------------


# Função para iniciar o programa de Velocidade
def iniciar_programa_velo():
    if entrada.get() == '':
        path_xml = r'C:\TV\XML\current.xml'
    else:
        path_xml = entrada.get()
    stop_thread_velo.clear()
    limpar_tela()
    # Abrir o navegador na página gerada
    time.sleep(1)  # Espera para garantir que o servidor esteja pronto
    webbrowser.open('http://127.0.0.1:5000/pagina_velocidade')
    threading.Thread(target=pegar_infos_piloto, args=(path_xml, stop_thread_velo, pitin.get(), timein.get(), pitout.get(), limite.get())).start()


# Função para reiniciar o programa de Velocidade
def reiniciar_programa_velo():
    if entrada.get() == '':
        path_xml = r'C:\TV\XML\current.xml'
    else:
        path_xml = entrada.get()
    stop_thread_velo.set()
    time.sleep(2)
    stop_thread_velo.clear()
    limpar_tela()
    threading.Thread(target=pegar_infos_piloto, args=(path_xml, stop_thread_velo)).start()


# Função para finalizar o programa de Velocidade
def finalizar_programa_velo():
    print('Stopped')
    stop_thread_velo.set()

# ---------------------GUI------------------------------------


# Criando interface com CustomTKInter
root = ctk.CTk()
root.title("Cronobox Assistant")
root.geometry("700x600")
root.resizable(width=False, height=False)
ctk.set_appearance_mode('dark')

# Frames Top e Bottom
top_frame = ctk.CTkFrame(master=root, fg_color='transparent')
top_frame.pack(side='top', fill='both', expand=True)

bottom_frame = ctk.CTkFrame(master=root, fg_color='transparent')
bottom_frame.pack(side='top', fill='both', expand=True)

# ---------------------Labels e Inputs Top Frame------------------------------------

# Label e input para XML Current
label = ctk.CTkLabel(top_frame, text='Digite o caminho do XML Current:')
label.pack()

entrada = ctk.CTkEntry(top_frame, width=600)
entrada.pack()

# Informativo sobre os caminhos padrões
info_label = ctk.CTkLabel(top_frame, text=r'* Deixar em branco usa caminhos padrão: C:\TV\XML e C:\TV\XML\Extras')
info_label.pack()

iniciar_server_btn = ctk.CTkButton(top_frame, text="START SERVER", font=("TkDefaultFont", 16, 'bold'), corner_radius=10, fg_color="#061cc2", hover_color="black", command=iniciar_server)
iniciar_server_btn.pack(side='top', anchor='n', pady=10, padx=100)

# ---------------------Control Buttons Middle Frame------------------------------------
buttons_frame = ctk.CTkFrame(bottom_frame, fg_color='transparent')
buttons_frame.pack(side='top', fill='x')

# Frame para botões de Safety
safety_frame = ctk.CTkFrame(buttons_frame, fg_color='transparent')
safety_frame.pack(side='left', fill='x', expand=True)

safety_label = ctk.CTkLabel(safety_frame, text='Controles Programa Safety', font=("TkDefaultFont", 14, 'bold'))
safety_label.pack(side='top', anchor='w', pady=10, padx=80)

iniciar_safety_btn = ctk.CTkButton(safety_frame, text="START", font=("TkDefaultFont", 16, 'bold'), corner_radius=10, fg_color="#636301", hover_color="black", command=iniciar_programa_safety)
iniciar_safety_btn.pack(side='top', anchor='w', pady=10, padx=100)

restart_safety_btn = ctk.CTkButton(safety_frame, text="RESTART", font=("TkDefaultFont", 16, 'bold'), corner_radius=10, fg_color="#636301", hover_color="black", command=reiniciar_programa_safety)
restart_safety_btn.pack(side='top', anchor='w', pady=10, padx=100)

finalizar_safety_btn = ctk.CTkButton(safety_frame, text="STOP", font=("TkDefaultFont", 16, 'bold'), corner_radius=10, fg_color="#636301", hover_color="black", command=finalizar_programa_safety)
finalizar_safety_btn.pack(side='top', anchor='w', pady=10, padx=100)

# Frame para botões de Velocidade
velo_frame = ctk.CTkFrame(buttons_frame, fg_color='transparent')
velo_frame.pack(side='right', fill='x', expand=True)

velo_label = ctk.CTkLabel(velo_frame, text='Controles Programa Velocidade', font=("TkDefaultFont", 14, 'bold'))
velo_label.pack(side='top', anchor='e', pady=10, padx=50)

iniciar_velo_btn = ctk.CTkButton(velo_frame, text="START", font=("TkDefaultFont", 16, 'bold'), fg_color="#750202", corner_radius=10, hover_color="black", command=iniciar_programa_velo)
iniciar_velo_btn.pack(side='top', anchor='e', pady=10, padx=100)

restart_velo_btn = ctk.CTkButton(velo_frame, text="RESTART", font=("TkDefaultFont", 16, 'bold'), fg_color="#750202", corner_radius=10, hover_color="black", command=reiniciar_programa_velo)
restart_velo_btn.pack(side='top', anchor='e', pady=10, padx=100)

finalizar_velo_btn = ctk.CTkButton(velo_frame, text="STOP", font=("TkDefaultFont", 16, 'bold'), fg_color="#750202", corner_radius=10, hover_color="black", command=finalizar_programa_velo)
finalizar_velo_btn.pack(side='top', anchor='e', pady=10, padx=100)

# ---------------------Check e Inputs Bottom Frame------------------------------------

# Frame para Campos de entrada
entries_frame = ctk.CTkFrame(bottom_frame, fg_color='transparent')
entries_frame.pack(side='top', fill='x')

# Frame para Campos de entrada
dist_frame = ctk.CTkFrame(entries_frame, fg_color='transparent')
dist_frame.pack(side='right', fill='x', expand=True)

# Campos de entrada
pitin_label = ctk.CTkLabel(dist_frame, text='Distância Pit In (m):')
pitin_label.pack(side='top', anchor='e', padx=115)
pitin = ctk.CTkEntry(dist_frame)
pitin.pack(side='top', anchor='e', padx=100)


timein_label = ctk.CTkLabel(dist_frame, text='Distância Time In (m):')
timein_label.pack(side='top', anchor='e', padx=105)
timein = ctk.CTkEntry(dist_frame)
timein.pack(side='top', anchor='e', padx=100)

pitout_label = ctk.CTkLabel(dist_frame, text='Distância Pit Out (m):')
pitout_label.pack(side='top', anchor='e', padx=110)
pitout = ctk.CTkEntry(dist_frame)
pitout.pack(side='top', anchor='e', padx=100)

limite_label = ctk.CTkLabel(dist_frame, text='Velocidade Limite (km/h):')
limite_label.pack(side='top', anchor='e', padx=100)
limite = ctk.CTkEntry(dist_frame)
limite.pack(side='top', anchor='e', padx=100)

# Frame para Check Safety Line
line_frame = ctk.CTkFrame(entries_frame, fg_color='transparent')
line_frame.pack(side='left', fill='x', expand=True)

line_box = ctk.CTkCheckBox(line_frame, text='Safety Line na pista?')
line_box.pack(side='top', anchor='w', pady=20, padx=100)


if __name__ == "__main__":
    root.mainloop()





