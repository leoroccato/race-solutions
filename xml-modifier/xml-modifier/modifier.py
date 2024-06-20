import sys
import threading
import time
import logging
import customtkinter as ctk
from customtkinter import filedialog
import xml.etree.ElementTree as ET

# TODO: Concatenar valor na frente e atrás


# Criando logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),  # log file
                    ])
logger = logging.getLogger(__name__)


class XMLModifierApp(ctk.CTk):

    # Function for open dialog to browse
    def open_file_dialog(self):
        try:
            logger.info('Browsing for file')
            file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
            if file_path:
                self.input_path_entry.delete(0, ctk.END)
                self.input_path_entry.insert(0, file_path)
            else:
                logger.warning('No file found')
        except Exception as e:
            logger.error(f'Error selecting file: {e}')

    # Function for loading XML
    def load_xml(self):
        try:
            logger.info('Loading XML')
            # Carregar o XML de entrada
            input_path = self.input_path_entry.get()
            tree = ET.parse(input_path)
            root = tree.getroot()
            self.fields = []
            # Para cada campo
            for label in root.findall('.//label'):
                self.fields.append(label.attrib['type'])
            for column in root.find('.//columns').attrib:
                self.fields.append(column)
            # Certifique-se de que fields não esteja vazio e contenha strings
            if not self.fields:
                logger.warning('No fields found in XML')
                return
            logger.debug(f'Fields found: {self.fields}')
            # Configurar os valores dos comboboxes
            for combobox in self.comboboxes:
                combobox.configure(values=self.fields)
                logger.debug(f'Combobox {combobox} configured with values: {combobox.cget("values")}')
                combobox.set('')
            logger.info('Comboboxes updated with fields from XML')
        except Exception as e:
            logger.error(f'Error loading XML file: {e}')

    # Function to add a new modification
    def add_modification(self):
        try:
            logger.info('Adding modifications')

            # Coleta as modificações dos 5 conjuntos de campos
            modifications = []
            for i in range(5):
                prefixo = self.prefix_entries[i].get()
                selected_field = self.comboboxes[i].get()
                sufixo = self.sufix_entries[i].get()

                if prefixo and selected_field and sufixo:
                    modification = (prefixo, selected_field, sufixo)
                    modifications.append(modification)
                    # Limpa os campos
                    self.prefix_entries[i].delete(0, ctk.END)
                    self.comboboxes[i].set('')
                    self.sufix_entries[i].delete(0, ctk.END)
                    logger.debug(f'Modification added: {modification}')
                    print(f'Modification added: {modification}')
                else:
                    logger.warning(f'Missing field or value in set {i + 1}')

            if modifications:
                self.modifications.extend(modifications)
            else:
                logger.warning('No modifications to add')

        except Exception as e:
            logger.error(f'Error adding modifications: {e}')

    # Function to start modifying
    def start_modifying(self):
        try:
            logger.info('Starting thread')
            if not self.modifying:
                self.modifying = True
                thread = threading.Thread(target=self.modify_xml_continuously)
                thread.start()
        except Exception as e:
            logger.error(f'Error starting thread: {e}')

    # Function to keep looping
    def modify_xml_continuously(self):
        try:
            input_path = self.input_path_entry.get()
            output_path = self.output_path_entry.get()
            while self.modifying:
                # Load XML
                tree = ET.parse(input_path)
                root = tree.getroot()
                for modification in self.modifications:
                    field, value = modification
                    for label in root.findall('.//label'):
                        if label.attrib['type'] == field:
                            if label.text is None:
                                label.text = ""
                            label.text += value
                    for result in root.findall('.//result'):
                        if field in result.attrib:
                            if result.attrib[field] is None:
                                result.attrib[field] = ""
                            result.attrib[field] += value
                    # Save the new XML
                    tree.write(output_path)
                    logger.info(f'New XML saved as {output_path}')
                    time.sleep(1)
        except Exception as e:
            logger.error(f'Error executing the program: {e}')

    # Function to stop modifying
    def stop_modifying(self):
        self.modifying = False
        self.destroy()
        sys.exit()

    def __init__(self):
        super().__init__()

        # ------------------------------DEFINE BASIC ATTRIBUTES

        self.title("XML Modifier")
        self.geometry("500x600")
        self.resizable(width=False, height=False)

        # Listas para armazenar widgets
        self.prefix_entries = []
        self.comboboxes = []
        self.suffix_entries = []
        self.fields = ['meu ovo', 'direito', 'esquerdo']

        # ------------------------------DEFINE FRAMES

        top_frame = ctk.CTkFrame(master=self, fg_color='transparent')
        top_frame.pack(side='top', fill='both', expand=False)
        bottom_frame = ctk.CTkFrame(master=self, fg_color='transparent')
        bottom_frame.pack(side='top', fill='both', expand=True)
        bottom_left_frame = ctk.CTkFrame(master=bottom_frame, fg_color='transparent')
        bottom_left_frame.pack(side='left', fill='both')
        bottom_center_frame = ctk.CTkFrame(master=bottom_frame, fg_color='transparent')
        bottom_center_frame.pack(side='left', fill='both')
        bottom_right_frame = ctk.CTkFrame(master=bottom_frame, fg_color='transparent')
        bottom_right_frame.pack(side='left', fill='both')

        # ------------------------------TOP FRAME ELEMENTS

        # Input frame label and entry
        self.input_path_label = ctk.CTkLabel(top_frame, text="Input XML Path:")
        self.input_path_label.pack(side='top', fill='x', expand=False)

        self.input_path_entry = ctk.CTkEntry(top_frame)
        self.input_path_entry.pack(side='top', fill='x', expand=False)

        # Botão para abrir o diálogo de seleção de arquivo
        self.btn_browse = ctk.CTkButton(top_frame, text="Browse Input", command=self.open_file_dialog)
        self.btn_browse.pack(side='top', pady=10)

        # Button for loading XML
        self.load = ctk.CTkButton(top_frame, text="Load XML", command=self.load_xml)
        self.load.pack(side='top', pady=10)

        # Output path label and entry
        self.output_path_label = ctk.CTkLabel(top_frame, text="Output XML Path:")
        self.output_path_label.pack(side='top', fill='x', expand=False)

        self.output_path_entry = ctk.CTkEntry(top_frame)
        self.output_path_entry.pack(side='top', fill='x', expand=False)

        # -----------------------------BOTTOM LEFT FRAME ELEMENTS

        # Enter what value to alter
        self.value_label = ctk.CTkLabel(bottom_left_frame, text="Prefix:")
        self.value_label.pack(side='top', anchor='w', expand=False, pady=10, padx=15)

        for i in range(5):
            prefix_entry = ctk.CTkEntry(bottom_left_frame)
            prefix_entry.pack(side='top', anchor='w', expand=False, pady=5, padx=15)
            self.prefix_entries.append(prefix_entry)

        # Button to start modifying
        self.modify_button = ctk.CTkButton(bottom_left_frame, text="Start", command=self.start_modifying)
        self.modify_button.pack(side='top', anchor='w', expand=False, pady=10, padx=15)

        # -----------------------------BOTTOM CENTER FRAME ELEMENTS

        # Select which field to alter
        self.field_label = ctk.CTkLabel(bottom_center_frame, text="XML Fields:")
        self.field_label.pack(side='top', anchor='w', expand=False, pady=10, padx=15)

        for i in range(5):
            combobox = ctk.CTkComboBox(bottom_center_frame, values=self.fields)
            combobox.pack(side='top', anchor='w', expand=False, pady=5, padx=15)
            self.comboboxes.append(combobox)

        self.label_running = ctk.CTkLabel(bottom_center_frame, text='Runnning...')
        self.label_running.pack(side='top', anchor='w', expand=False, pady=10, padx=35)

        # -----------------------------BOTTOM RIGHT FRAME ELEMENTS

        # Enter what value to alter
        self.value_label = ctk.CTkLabel(bottom_right_frame, text="Sufix:")
        self.value_label.pack(side='top', anchor='w', expand=False, pady=10, padx=15)

        for i in range(5):
            suffix_entry = ctk.CTkEntry(bottom_right_frame)
            suffix_entry.pack(side='top', anchor='w', expand=False, pady=5, padx=15)
            self.suffix_entries.append(suffix_entry)

        # Button to stop modifying
        self.stop_button = ctk.CTkButton(bottom_right_frame, text="Stop", command=self.stop_modifying)
        self.stop_button.pack(side='top', anchor='w', expand=False, pady=10, padx=15)

        self.modifications = []

        self.prefix_entries = [ctk.CTkEntry(self) for _ in range(5)]
        self.comboboxes = [ctk.CTkComboBox(self) for _ in range(5)]
        self.sufix_entries = [ctk.CTkEntry(self) for _ in range(5)]

        self.modifying = False


if __name__ == "__main__":
    app = XMLModifierApp()
    app.mainloop()
