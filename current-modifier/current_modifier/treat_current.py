import xml.etree.ElementTree as ET

# Carregar o XML de entrada
tree = ET.parse(r'C:\TV\XML\current.xml')
root = tree.getroot()

fields = []

for label in root.findall('.//label'):
    fields.append(label.attrib['type'])

for column in root.find('.//columns').attrib:
    fields.append(column)

print("Campos disponíveis:", fields)

