import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import os


def run_script_in_thread():
    def run_script():
        os.environ['PYTHONPATH'] = r"C:\Users\leoro\Desktop\Projetos\Cronometragem\Python\pythonCronobox\.venv\Lib\site-packages" + os.pathsep + os.environ.get('PYTHONPATH', '')
        subprocess.run(["python", "getLive_API_report.py"])
    thread = threading.Thread(target=run_script)
    thread.start()

def stop_script():
    global process
    if process is not None:
        process.terminate()  # Envia sinal para terminar o processo
        process = None

root = tk.Tk()
root.title("Cronobox Meteorologia")
root.geometry("700x500")  # Define o tamanho da janela

# Criar um rótulo
label_event = tk.Label(root, text="Selecione o Evento:")
label_event.pack(pady=(10, 0))

# Lista de eventos (mockup para exemplo)
eventos = ["Evento 1", "Evento 2", "Evento 3"]
event_var = tk.StringVar(value=eventos)
listbox = tk.Listbox(root, listvariable=event_var, height=3)
listbox.pack()

label_path = tk.Label(root, text="Insira a :")
label_path.pack(pady=(10, 0))

entry_path = tk.Entry(root, width=50)
entry_path.pack()

def browse_file():
    filepath = filedialog.askopenfilename()
    entry_path.delete(0, tk.END)
    entry_path.insert(0, filepath)


button_browse = tk.Button(root, text="Buscar", command=browse_file)
button_browse.pack(pady=(5, 10))

button_start = tk.Button(root, text="Iniciar", command=run_script_in_thread())
button_start.pack(pady=20)

button_stop = tk.Button(root, text="Parar", command=stop_script)
button_stop.pack(pady=20)

button_report = tk.Button(root, text="Gerar Relatório", command=lambda: print("Gerar Relatório"))
button_report.pack(side=tk.LEFT, padx=(10, 10), pady=(10, 10))

root.mainloop()
