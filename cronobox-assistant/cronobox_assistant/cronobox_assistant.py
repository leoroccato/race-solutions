# Padrão
import xml.etree.ElementTree as ET
import threading
import time

# Terceiros
import customtkinter as ctk

# Módulos
from safety_car_monitor import main_loop
from speed_monitor import pegar_infos_piloto


# Criando as Threads para eventos de Safety e Velocidade
stop_thread_safety = threading.Event()
stop_thread_velo = threading.Event()

# Instancia a classe SafetyCarMonitor
monitor = SafetyCarMonitor(path_xml='', path_xml_safety='')  # Inicialmente sem caminhos, serão definidos nas funções


# Função para limpar o XML Safety -> Limpar a tela
def limpar_xml(path_xml):
    # Carrega o arquivo XML
    tree = ET.parse(path_xml)
    raiz = tree.getroot()

    # Encontra o elemento <results>
    results = raiz.find('results')

    # Limpa todos os elementos filhos de <results>
    results.clear()

    # Salva as alterações de volta no arquivo
    tree.write(path_xml, encoding='utf-8', xml_declaration=True)


# ---------------------Funções Auxiliares de Controle------------------------------------

def iniciar_programa(path_xml, path_xml_safety, stop_thread, target_function):
    stop_thread.clear()
    limpar_xml(path_xml_safety)
    threading.Thread(target=target_function, args=(stop_thread,)).start()


def reiniciar_programa(path_xml, path_xml_safety, stop_thread, target_function):
    stop_thread.set()
    time.sleep(2)
    iniciar_programa(path_xml, path_xml_safety, stop_thread, target_function)


def finalizar_programa(stop_thread):
    stop_thread.set()

# ---------------------Funções de Controle Safety------------------------------------


def iniciar_programa_safety():
    monitor.path_xml = entrada.get() or r'C:\TV\XML\current.xml'
    monitor.path_xml_safety = entrada_safety.get() or r'C:\TV\XML\Extras\safety.xml'
    iniciar_programa(monitor.path_xml, monitor.path_xml_safety, stop_thread_safety, monitor.main_loop)

def reiniciar_programa_safety():
    monitor.path_xml = entrada.get() or r'C:\TV\XML\current.xml'
    monitor.path_xml_safety = entrada_safety.get() or r'C:\TV\XML\Extras\safety.xml'
    reiniciar_programa(monitor.path_xml, monitor.path_xml_safety, stop_thread_safety, monitor.main_loop)


def finalizar_programa_safety():
    finalizar_programa(stop_thread_safety)

# ---------------------Funções de Controle Velocidade------------------------------------


def iniciar_programa_velo():
    path_xml = entrada.get() or r'C:\TV\XML\current.xml'
    path_xml_velo = entrada_velo.get() or r'C:\TV\XML\Extras\velo.xml'
    iniciar_programa(path_xml, path_xml_velo, stop_thread_velo, pegar_infos_piloto)


def reiniciar_programa_velo():
    path_xml = entrada.get() or r'C:\TV\XML\current.xml'
    path_xml_velo = entrada_velo.get() or r'C:\TV\XML\Extras\velo.xml'
    reiniciar_programa(path_xml, path_xml_velo, stop_thread_velo, pegar_infos_piloto)


def finalizar_programa_velo():
    finalizar_programa(stop_thread_velo)


# ---------------------GUI------------------------------------

# ---------------------Funções Auxiliares GUI------------------------------------

def criar_label_input(frame, text, var_name):
    label = ctk.CTkLabel(frame, text=text)
    label.pack()
    entrada = ctk.CTkEntry(frame, width=600)
    entrada.pack()
    return entrada


def criar_botao(frame, text, command, fg_color):
    return ctk.CTkButton(frame, text=text, font=("TkDefaultFont", 16, 'bold'), corner_radius=10, fg_color=fg_color, hover_color="black", command=command)


def criar_frame_botoes(frame, label_text, commands, colors):
    sub_frame = ctk.CTkFrame(frame, fg_color='transparent')
    sub_frame.pack(side='left', fill='x', expand=True)
    label = ctk.CTkLabel(sub_frame, text=label_text, font=("TkDefaultFont", 14, 'bold'))
    label.pack(side='top', anchor='w', pady=10, padx=70)
    for text, command, color in zip(['START', 'RESTART', 'STOP'], commands, colors):
        btn = criar_botao(sub_frame, text, command, color)
        btn.pack(side='top', anchor='w', pady=10, padx=100)

# ---------------------Frames e Componentes GUI------------------------------------


# Inicialização da GUI
root = ctk.CTk()
root.title("Cronobox Assistant")
root.geometry("700x600")
root.resizable(width=False, height=False)
ctk.set_appearance_mode('dark')

# Frames Top e Bottom
top_frame = ctk.CTkFrame(master=root, fg_color='transparent')
bottom_frame = ctk.CTkFrame(master=root, fg_color='transparent')
bottom_frame.pack(side='top', fill='both', expand=True)

# Labels e entries para XML Current, Safety e Velocidade
labels = ['Digite o caminho do XML Current:', 'Digite o caminho do XML Safety:', 'Digite o caminho do XML Velocidade:']
label_texts = ['entrada', 'entrada_safety', 'entrada_velo']

# Inputs Top Frame
entradas = {}
for label_text, var_name in zip(labels, label_texts):
    entrada = criar_label_input(top_frame, label_text, var_name)
    entradas[var_name] = entrada

# Atribuição das variáveis globais
entrada = entradas['entrada']
entrada_safety = entradas['entrada_safety']
entrada_velo = entradas['entrada_velo']

# Informativo sobre os caminhos padrões
info_label = ctk.CTkLabel(top_frame, text=r'* Deixar em branco usa caminhos padrão: C:\TV\XML e C:\TV\XML\Extras')
info_label.pack()

# Frame para botões de Safety e Velocidade
commands_safety = [iniciar_programa_safety, reiniciar_programa_safety, finalizar_programa_safety]
colors_safety = ["#636301", "#636301", "#636301"]
commands_velo = [iniciar_programa_velo, reiniciar_programa_velo, finalizar_programa_velo]
colors_velo = ["#750202", "#750202", "#750202"]

buttons_frame = ctk.CTkFrame(bottom_frame, fg_color='transparent')
buttons_frame.pack(side='top', fill='x')

criar_frame_botoes(buttons_frame, 'Controles Programa Safety', commands_safety, colors_safety)
criar_frame_botoes(buttons_frame, 'Controles Programa Velocidade', commands_velo, colors_velo)

# Inputs Bottom Frame
entries_frame = ctk.CTkFrame(bottom_frame, fg_color='transparent')
entries_frame.pack(side='top', fill='x')

dist_frame = ctk.CTkFrame(entries_frame, fg_color='transparent')
dist_frame.pack(side='right', fill='x', expand=True)

entry_label_1 = ctk.CTkLabel(dist_frame, text='Distância Pit In (m):')
entry_label_1.pack(side='top', anchor='e', padx=115)
entry_1 = ctk.CTkEntry(dist_frame)
entry_1.pack(side='top', anchor='e', padx=100)

entry_label_2 = ctk.CTkLabel(dist_frame, text='Distância Time In (m):')
entry_label_2.pack(side='top', anchor='e', padx=105)
entry_2 = ctk.CTkEntry(dist_frame)
entry_2.pack(side='top', anchor='e', padx=100)

entry_label_3 = ctk.CTkLabel(dist_frame, text='Distância Pit Out (m):')
entry_label_3.pack(side='top', anchor='e', padx=110)
entry_3 = ctk.CTkEntry(dist_frame)
entry_3.pack(side='top', anchor='e', padx=100)

line_frame = ctk.CTkFrame(entries_frame, fg_color='transparent')
line_frame.pack(side='left', fill='x', expand=True)

line_box = ctk.CTkCheckBox(line_frame, text='Safety Line na pista?')
line_box.pack(side='top', anchor='w', pady=20, padx=100)

if __name__ == "__main__":
    root.mainloop()






