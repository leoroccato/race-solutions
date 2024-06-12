import threading
import time
import customtkinter as ctk
import xml.etree.ElementTree as ET

# Carregar o XML de entrada
tree = ET.parse('current.xml')
root = tree.getroot()

# Mapear os campos disponíveis
fields = []

for label in root.findall('.//label'):
    fields.append(label.attrib['type'])

for column in root.find('.//columns').attrib:
    fields.append(column)


class XMLModifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("XML Modifier")
        self.geometry("700x500")

        # Input path label and entry
        self.input_path_label = ctk.CTkLabel(self, text="Input XML Path:")
        self.input_path_label.grid(row=0, column=0, padx=10, pady=10)

        self.input_path_entry = ctk.CTkEntry(self)
        self.input_path_entry.grid(row=0, column=1, padx=10, pady=10)

        # Output path label and entry
        self.output_path_label = ctk.CTkLabel(self, text="Output XML Path:")
        self.output_path_label.grid(row=1, column=0, padx=10, pady=10)

        self.output_path_entry = ctk.CTkEntry(self)
        self.output_path_entry.grid(row=1, column=1, padx=10, pady=10)

        self.field_label = ctk.CTkLabel(self, text="Select Field:")
        self.field_label.grid(row=2, column=0, padx=10, pady=10)

        self.field_combobox = ctk.CTkComboBox(self, values=fields)
        self.field_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.value_label = ctk.CTkLabel(self, text="Enter Value to Concatenate:")
        self.value_label.grid(row=3, column=0, padx=10, pady=10)

        self.value_entry = ctk.CTkEntry(self)
        self.value_entry.grid(row=3, column=1, padx=10, pady=10)

        self.add_button = ctk.CTkButton(self, text="Add Modification", command=self.add_modification)
        self.add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.modification_listbox = ctk.CTkTextbox(self, height=50)
        self.modification_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.modify_button = ctk.CTkButton(self, text="Modify XML", command=self.start_modifying)
        self.modify_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop", command=self.stop_modifying)
        self.stop_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.modifications = []
        self.modifying = False

    def add_modification(self):
        selected_field = self.field_combobox.get()
        new_value = self.value_entry.get()
        if selected_field and new_value:
            modification = (selected_field, new_value)
            self.modifications.append(modification)
            self.modification_listbox.insert(ctk.END, f"{selected_field}: {new_value}")
            self.field_combobox.set('')
            self.value_entry.delete(0, ctk.END)

    def start_modifying(self):
        if not self.modifying:
            self.modifying = True
            thread = threading.Thread(target=self.modify_xml_continuously)
            thread.start()

    def modify_xml_continuously(self):
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

                # Salvar o novo XML
                tree.write(output_path)
                print(f"XML modificado salvo como '{output_path}'")

                # Esperar um curto período antes da próxima modificação
                time.sleep(0.1)  # Ajuste o intervalo conforme necessário

    def stop_modifying(self):
        self.modifying = False

if __name__ == "__main__":
    app = XMLModifierApp()
    app.mainloop()
