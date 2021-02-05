import subprocess
import sys
import uuid
from namespaces import namespaces
import xml.etree.ElementTree as ET

def run(command, dir='.'):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, cwd=dir)
    output, error = process.communicate()
    if error is not None:
        print(output)
        print(error)

filename = sys.argv[1]
section_index = sys.argv[2]

tmp_dir = uuid.uuid4().hex
unzip_cmd = "unzip " + filename + " -d " + tmp_dir
run(unzip_cmd)

for namespace in namespaces:
    ET.register_namespace(namespace, namespaces[namespace])

tree = ET.parse(tmp_dir + "/content.xml")
root = tree.getroot()

a_s = root.findall('office:automatic-styles/style:style[@style:family="section"]', namespaces)
#print(ET.tostring(a_s[int(section_index)-1], encoding="utf-8", method="xml"))
section = a_s[int(section_index) - 1]
props = section.find("style:section-properties", namespaces)
if props.attrib["{0}editable".format("{" + namespaces["style"] + "}")] == "true":
    props.attrib["{0}editable".format("{" + namespaces["style"] + "}")] = "false"
else:
    props.attrib["{0}editable".format("{" + namespaces["style"] + "}")] = "true"

content_file = open(tmp_dir + "/content.xml", "wb")
data = ET.tostring(root, encoding='UTF-8', method='xml')
content_file.write(data)

zip_cmd = "zip -r " + filename + " ."
run(zip_cmd, tmp_dir)

mv_cmd = "mv " + tmp_dir + "/" + filename + " ."
run(mv_cmd)

rm_cmd = "rm -rf " + tmp_dir
run(rm_cmd)
