#==============================
#Author: Team 3
#Member: Nathan, Neha, Tri, Yaqi
#Date: 10/18/2015
#==============================


from hl7apy.parser import parse_segments
from pymongo import MongoClient
from datetime import datetime
import json
import os

def get_msg(f):
    numlines = 4
    hl7msg = ""
    infile = open(f,'r')
    for index, line in enumerate(infile):
        if index < numlines:
            hl7msg += line
    hl7msg = hl7msg.replace("\n", "\r")
    infile.close()
    return hl7msg


def parseHL7(hl7_msg=""):
    """Parses an HL7 message into a JSON-LD document suitable for persisting
    into MongoDB
    hl7_msg -- a string containing the HL7 message to be parsed
    Returns a python dictionary representing the document to be stored
    """
    msg = parse_segments(hl7_msg)
    MSH = msg[0]
    PID = msg[1]
    OBX = msg[2]
    OBR = msg[3]

    MRN = PID.pid_3.pid_3_1.to_er7()
    SEX = PID.pid_8.to_er7()
    dob = PID.pid_7.to_er7()
    DOB = str(datetime.strptime(dob, '%Y%m%d').date())
    TestValue = OBX.obx_5.to_er7()
    LOINC_Code = OBR.obr_4.obr_4_1.to_er7()
    DES = OBR.obr_4.obr_4_2.to_er7()

    patient = {"resourceType": "Patient", "identifier": [ {"use": "usual", "label": "MRN", "system": "urn:oid:2.16.840.1.113883.19.5",
    "value": MRN}], "gender": {"coding":[ {"system": "http://hl7.org/fhir/v3/AdministrativeGender", "code":SEX}]},
    "birthDate": DOB, "managingOrganization": {"reference": "Organization/2.16.840.1.113883.19.5","display": "MIMIC2"},}

    observation = {"resourceType":  "Observation", "name": { "coding": [ { "system" : "http://loinc.org", "code" : LOINC_Code, "display": DES}]},
    "valueQuantity": { "value" : TestValue,}, "issued": "2013-04-03T15:30:10+01:00", "status": "final", "subject": { "reference": "Patient/" + MRN,
    "display" : "P. van de Heuvel"},}

    return [patient,observation]


def save(record):

    #Establish connection to  running mongod instance
    client = MongoClient()
    #Establish connection to HL7Lab_Team3 database. The first time the database will be created.
    db = client.HL7Lab_Team3



    #insert document into the HL7Lab collection. The first time the collection will be created.
    if isinstance(record,dict):
        result = db.HL7Lab.insert(record)
    elif isinstance(record,list):
        for elem in record:
            db.HL7Lab.insert(elem)

    #print ("== Record Saved ==")




def showCollections ():

    print("== Display all documents within collections ==")
    client = MongoClient()
    db = client.HL7Lab_Team3
    cursor = db.HL7Lab.find()
    for document in cursor:
        print(document)



