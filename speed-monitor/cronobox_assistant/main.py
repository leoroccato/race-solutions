# Padrão
import webbrowser
import threading
import time
import requests
# Terceiros
import customtkinter as ctk
# Módulos
from server import run_server
from speed_monitor import pegar_infos_piloto

# Flags de controle das threads de eventos
stop_thread_velo = threading.Event()

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


# ---------------------Velocidade Controls------------------------------------


# Função para iniciar o programa de Velocidade
def iniciar_programa_velo():
    if entrada.get() == '':
        path_xml = r'C:\TV\XML\current.xml'
    else:
        path_xml = entrada.get()
    # Coletando as distâncias dos campos de entrada
    distancias = [
        first.get(),
        second.get(),
        third.get(),
        limite.get()
    ]

    # Coletando as seleções dos comboboxes
    comboboxes = [
        combobox1.get(),
        combobox2.get(),
        combobox3.get(),
        combobox4.get()
    ]

    # Coletando as strings adicionais dos campos de entrada
    strings = [
        string1.get(),
        string2.get(),
        string3.get(),
        string4.get()
    ]
    stop_thread_velo.clear()
    limpar_tela()
    # Abrir o navegador na página gerada
    time.sleep(1)  # Espera para garantir que o servidor esteja pronto
    webbrowser.open('http://127.0.0.1:5000/pagina_velocidade')
    threading.Thread(target=pegar_infos_piloto, args=(path_xml, stop_thread_velo, distancias, comboboxes, strings, limite)).start()


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

# Frame para botões de Velocidade
velo_frame = ctk.CTkFrame(buttons_frame, fg_color='transparent')
velo_frame.pack(side='top', fill='x', expand=True)

velo_label = ctk.CTkLabel(velo_frame, text='Controles Programa Velocidade', font=("TkDefaultFont", 14, 'bold'))
velo_label.pack(side='top', pady=10, padx=50)

iniciar_velo_btn = ctk.CTkButton(velo_frame, text="START", font=("TkDefaultFont", 16, 'bold'), fg_color="#750202", corner_radius=10, hover_color="black", command=iniciar_programa_velo)
iniciar_velo_btn.pack(side='top', pady=10, padx=100)

restart_velo_btn = ctk.CTkButton(velo_frame, text="RESTART", font=("TkDefaultFont", 16, 'bold'), fg_color="#750202", corner_radius=10, hover_color="black", command=reiniciar_programa_velo)
restart_velo_btn.pack(side='top', pady=10, padx=100)

finalizar_velo_btn = ctk.CTkButton(velo_frame, text="STOP", font=("TkDefaultFont", 16, 'bold'), fg_color="#750202", corner_radius=10, hover_color="black", command=finalizar_programa_velo)
finalizar_velo_btn.pack(side='top', pady=10, padx=100)

# ---------------------Check e Inputs Bottom Frame------------------------------------

# Frame para Campos de entrada
entries_frame = ctk.CTkFrame(bottom_frame, fg_color='transparent')
entries_frame.pack(side='top', fill='x')

# Frame para os comboboxes à esquerda
combobox_frame = ctk.CTkFrame(entries_frame, fg_color='transparent')
combobox_frame.pack(side='left', padx=20, pady=10)

# Frame para os campos de entrada centralizados
dist_frame = ctk.CTkFrame(entries_frame, fg_color='transparent')
dist_frame.pack(side='left', padx=20, pady=10, expand=True)

# Frame para os campos de entrada de string à direita
string_frame = ctk.CTkFrame(entries_frame, fg_color='transparent')
string_frame.pack(side='left', padx=20, pady=10)

# Comboboxes à esquerda
combobox1 = ctk.CTkComboBox(combobox_frame, values=["Setor 3", "Setor 4", "Setor 5", "Setor 6"])
combobox1.pack(anchor='w', pady=5)

combobox2 = ctk.CTkComboBox(combobox_frame, values=["Setor 3", "Setor 4", "Setor 5", "Setor 6"])
combobox2.pack(anchor='w', pady=5)

combobox3 = ctk.CTkComboBox(combobox_frame, values=["Setor 3", "Setor 4", "Setor 5", "Setor 6"])
combobox3.pack(anchor='w', pady=5)

combobox4 = ctk.CTkComboBox(combobox_frame, values=["Setor 3", "Setor 4", "Setor 5", "Setor 6"])
combobox4.pack(anchor='w', pady=5)

# Labels e Campos de entrada centralizados
first_label = ctk.CTkLabel(dist_frame, text='Distância (m):')
first_label.pack(anchor='center')

first = ctk.CTkEntry(dist_frame)
first.pack(anchor='center')

second_label = ctk.CTkLabel(dist_frame, text='Distância (m):')
second_label.pack(anchor='center')

second = ctk.CTkEntry(dist_frame)
second.pack(anchor='center')

third_label = ctk.CTkLabel(dist_frame, text='Distância (m):')
third_label.pack(anchor='center')

third = ctk.CTkEntry(dist_frame)
third.pack(anchor='center')

limite_label = ctk.CTkLabel(dist_frame, text='Velocidade Limite (km/h):')
limite_label.pack(anchor='center')

limite = ctk.CTkEntry(dist_frame)
limite.pack(anchor='center', pady=5)

# Campos de entrada de string à direita
string1 = ctk.CTkEntry(string_frame)
string1.pack(anchor='w', pady=5)

string2 = ctk.CTkEntry(string_frame)
string2.pack(anchor='w', pady=5)

string3 = ctk.CTkEntry(string_frame)
string3.pack(anchor='w', pady=5)

string4 = ctk.CTkEntry(string_frame)
string4.pack(anchor='w', pady=5)





if __name__ == "__main__":
    root.mainloop()





