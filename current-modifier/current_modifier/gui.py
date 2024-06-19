import threading
import time
import customtkinter as ctk
from customtkinter import filedialog
import xml.etree.ElementTree as ET


# TODO:

running = None
loaded = False


class XMLModifierApp(ctk.CTk):
    # Function for open dialog to browse
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.input_path_entry.delete(0, ctk.END)
            self.input_path_entry.insert(0, file_path)

    # Function for loading XML
    def load_xml(self):
        try:
            # Carregar o XML de entrada
            input_path = self.input_path_entry.get()
            tree = ET.parse(input_path)
            root = tree.getroot()
            fields = []
            # Para cada campo
            for label in root.findall('.//label'):
                fields.append(label.attrib['type'])
            for column in root.find('.//columns').attrib:
                fields.append(column)
            self.field_combobox.configure(values=fields)
        except Exception as e:
            print('Não consegui carregar XML')

    # Function to add a new modification
    def add_modification(self):
        selected_field = self.field_combobox.get()
        new_value = self.value_entry.get()
        if selected_field and new_value:
            modification = (selected_field, new_value)
            self.modifications.append(modification)
            self.modification_listbox.insert(ctk.END, f"{selected_field}: {new_value}")
            self.modification_listbox.insert(ctk.END, "\n")
            self.field_combobox.set('')
            self.value_entry.delete(0, ctk.END)

    # Function to start modifying
    def start_modifying(self):
        if not self.modifying:
            self.modifying = True
            thread = threading.Thread(target=self.modify_xml_continuously)
            thread.start()

    # Function to keep looping
    def modify_xml_continuously(self):
        try:
            running = "Running"
            input_path = self.input_path_entry.get()
            output_path = self.output_path_entry.get()
            while self.modifying:
                # Carregar o XML de entrada
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
                    print(f"XML modificado salvo como '{output_path}'")
                    # Esperar um curto período antes da próxima modificação
                    time.sleep(0.1)  # Ajuste o intervalo conforme necessário
        except Exception as e:
            running = "Erro"

    # Function to stop modifying
    def stop_modifying(self):
        self.modifying = False

    def __init__(self):
        super().__init__()

        # ------------------------------DEFINE BASIC ATTRIBUTES

        self.title("XML Modifier")
        self.geometry("700x500")
        self.resizable(width=False, height=False)

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
        self.btn_browse = ctk.CTkButton(top_frame, text="Browse", command=self.open_file_dialog)
        self.btn_browse.pack(side='top', pady=10)

        # Button for loading XML
        self.load = ctk.CTkButton(top_frame, text="Load XML", command=self.load_xml)
        self.load.pack(side='top', pady=10)

        # Output path label and entry
        self.output_path_label = ctk.CTkLabel(top_frame, text="Output XML Path:")
        self.output_path_label.pack(side='top', fill='x', expand=False)

        self.output_path_entry = ctk.CTkEntry(top_frame)
        self.output_path_entry.pack(side='top', fill='x', expand=False)

        # Botão para abrir o diálogo de seleção de arquivo
        self.btn_browse = ctk.CTkButton(top_frame, text="Browse", command=self.open_file_dialog)
        self.btn_browse.pack(side='top', pady=10)

        # -----------------------------BOTTOM LEFT FRAME ELEMENTS

        # Select which field to alter
        self.field_label = ctk.CTkLabel(bottom_left_frame, text="Select Field:")
        self.field_label.pack(side='top', anchor='w', expand=False, pady=5, padx=10)

        self.field_combobox = ctk.CTkComboBox(bottom_left_frame)
        self.field_combobox.pack(side='top', anchor='w', expand=False, pady=5, padx=10)

        # Enter what value to alter
        self.value_label = ctk.CTkLabel(bottom_left_frame, text="Enter Value to Concatenate:")
        self.value_label.pack(side='top', anchor='w', expand=False, pady=5, padx=10)

        self.value_entry = ctk.CTkEntry(bottom_left_frame)
        self.value_entry.pack(side='top', anchor='w', expand=False, pady=5, padx=10)

        # Button to Add a new Modification
        self.add_button = ctk.CTkButton(bottom_left_frame, text="Add Modification", command=self.add_modification)
        self.add_button.pack(side='top', anchor='w', expand=False, pady=5, padx=10)

        # -----------------------------BOTTOM CENTER FRAME ELEMENTS

        self.modification_listbox = ctk.CTkTextbox(bottom_center_frame, height=500)
        self.modification_listbox.pack(side='top', expand=False, pady=5)

        # -----------------------------BOTTOM RIGHT FRAME ELEMENTS

        # Button to start modifying
        self.modify_button = ctk.CTkButton(bottom_right_frame, text="Start", command=self.start_modifying)
        self.modify_button.pack(side='top', anchor='e', expand=False, pady=90, padx=10)

        # Button to stop modifying
        self.stop_button = ctk.CTkButton(bottom_right_frame, text="Stop", command=self.stop_modifying)
        self.stop_button.pack(side='top', anchor='e', expand=False, pady=0, padx=10)

        # Running label
        self.running_label = ctk.CTkLabel(bottom_frame, text=running)
        self.running_label.pack()

        self.modifications = []
        self.modifying = False


if __name__ == "__main__":
    app = XMLModifierApp()
    app.mainloop()
