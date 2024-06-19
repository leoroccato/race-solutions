import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET

def read_xml_and_fill_combobox(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        items =[]
        for label in root.findall('.//label'):
            items.append(label.attrib['type'])
        for column in root.find('.//columns').attrib:
            items.append(column)  # Ajuste o caminho conforme seu XML

        # Preenche a combobox
        combobox['values'] = items
        messagebox.showinfo("Sucesso", "Combobox preenchida com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao ler o XML: {e}")

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

def load_xml():
    file_path = entry_path.get()
    if file_path:
        read_xml_and_fill_combobox(file_path)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira o caminho do arquivo XML.")

# Inicializa a janela principal
root = tk.Tk()
root.title("Exemplo de Combobox com XML")

# Campo de entrada para o caminho do arquivo XML
entry_path = tk.Entry(root, width=50)
entry_path.pack(pady=10)

# Botão para abrir o diálogo de seleção de arquivo
btn_browse = tk.Button(root, text="Selecionar arquivo", command=open_file_dialog)
btn_browse.pack(pady=5)

# Botão para carregar o XML e preencher a combobox
btn_load = tk.Button(root, text="Carregar XML", command=load_xml)
btn_load.pack(pady=5)

# Cria a combobox
combobox = ttk.Combobox(root)
combobox.pack(pady=10)

# Inicializa o loop do Tkinter
root.mainloop()
