import docx2txt as docx
import os
import zipfile
import re
import xml.dom.minidom
import xmltodict
import person_details
import json

def to_text(filename):
    info = {}
    infoDict = {}
    text = docx.process("./static/"+filename)
    text = text.replace("\n"," ")
    infoDict['person'] = person_details.extract(text)
    document = zipfile.ZipFile("./static/"+filename)
    app = xmltodict.parse(xml.dom.minidom.parseString(document.read('docProps/app.xml')).toprettyxml(indent='  '))
    ja = json.loads(json.dumps(app))
    lines = ja['Properties']['Lines']
    characters = ja['Properties']['Characters']
    words = ja['Properties']['Words']
    font = xmltodict.parse(xml.dom.minidom.parseString(document.read('word/fontTable.xml')).toprettyxml(indent='  '))
    jf = json.loads(json.dumps(font))
    font = []
    for i in jf['w:fonts']['w:font']:
        if (i['@w:name']) != 'Symbol':
            font.append(i['@w:name'])
    doc = xmltodict.parse(xml.dom.minidom.parseString(document.read('word/document.xml')).toprettyxml(indent='  '))
    j = json.loads(json.dumps(doc))
    if 'w:tbl' in list(list(j['w:document']['w:body'].keys())):
        table = len(j['w:document']['w:body']['w:tbl'])
    else:
        table = 0
    nimage = 0
    for i in document.namelist():
        if i[:10]=='word/media':
            nimage = nimage+1
    info['lines'] = lines
    info['characters'] = characters
    info['words'] = words
    info['fonts'] = font
    info['table_count'] = table
    info['image_count'] = nimage
    infoDict['docx_details'] = info
    return infoDict