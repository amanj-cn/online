import subprocess
import uuid
from namespaces import namespaces
import xml.etree.ElementTree as ET

def run(command, dir='.'):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, cwd=dir)
    output, error = process.communicate()
    if error is not None:
        print(output)
        print(error)

def toggle_lock(filename, section_index):
    tmp_dir = uuid.uuid4().hex
    unzip_cmd = "unzip " + filename + " -d " + tmp_dir
    run(unzip_cmd)

    tree = ET.parse(tmp_dir + "/content.xml")
    root = tree.getroot()

    sections = root.findall('.//text:section', namespaces)
    # print(ET.tostring(sections[int(section_index)-1], encoding="utf-8", method="xml"))
    section = sections[int(section_index) - 1]
    if section.attrib["{0}protected".format("{" + namespaces["text"] + "}")] == "true":
        section.attrib["{0}protected".format("{" + namespaces["text"] + "}")] = "false"
    else:
        section.attrib["{0}protected".format("{" + namespaces["text"] + "}")] = "true"

    content_file = open(tmp_dir + "/content.xml", "wb")
    data = ET.tostring(root, encoding='UTF-8', method='xml')
    content_file.write(data)

    zip_cmd = "zip -r " + filename + " ."
    run(zip_cmd, tmp_dir)

    mv_cmd = "mv " + tmp_dir + "/" + filename + " ."
    run(mv_cmd)

    rm_cmd = "rm -rf " + tmp_dir
    run(rm_cmd)