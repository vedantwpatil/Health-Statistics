import xml.etree.ElementTree as ET

tree = ET.parse("../assets/apple_health_export/export.xml")
root = tree.getroot()

for element in root.iter():
    pass
