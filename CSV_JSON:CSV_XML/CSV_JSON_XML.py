from sys import argv
import csv
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom


def csv2json(f):
    infile = open(f,'r')
    reader = csv.DictReader(infile)
    records = []                           
    for row in reader:
        for key in row.keys():
            if row[key] == "":       
                del row[key]
        records.append({'patient':row})     
    main = json.dumps({'records':records}, indent = 4) 
    infile.close()
    return main


def csv2xml(f):
    infile = open(f,'r')
    reader = csv.reader(infile)  
    label = reader.next()    

    root = ET.Element('records')
    for row in reader:
        patient = ET.SubElement(root, "patient")
        for column in range(len(label)):
            if row[column]:
                child = ET.SubElement(patient, label[column]) 
                child.text = row[column]                   
    infile.close()
    return minidom.parseString(ET.tostring(root)).toprettyxml()

    
if __name__ == "__main__":

    csvfile = argv[1]
    formt = argv[2]

    if formt.lower() == "json":
        print csv2json(csvfile)
    if formt.lower() == "xml":
        print csv2xml(csvfile)


                               
    
        

