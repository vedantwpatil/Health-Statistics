import xml.etree.ElementTree as ET

tree = ET.parse("../../data/apple_health_export/export.xml")
root = tree.getroot()

for element in root.iter("Record"):
    print(element)

print("Finished")
