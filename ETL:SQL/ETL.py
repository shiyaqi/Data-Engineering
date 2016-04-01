import sqlite3,csv
def icd_text(num):
    string = str(num)
    length = len(string)
    if length == 3:
        return string
    else:
        text = string[:3]+'.'+string[3:]
        return text


conn = sqlite3.connect('safe-mimic.db')
cur = conn.cursor()


with open('patients.csv','rb') as p:
     preader = csv.reader(p)
     ptitle = preader.next()
     for row in preader:
         ID = row[0]
         gender = row[2]
         dob = row[1]
         p_record = [ID,gender,dob,'','','','']
         cur.execute( "INSERT INTO PATIENTS VALUES (?,?,?,?,?,?,?)", p_record)


with open('admissions.csv','rb') as a:
    areader = csv.reader(a)
    atitle = areader.next()
    icd_records = []
    for row in areader:
        sub_id = row[0]
        ha_id = row[1]
        addm_time = row[2]
        disch_time = row[3]
        ad_record = ['',sub_id,ha_id,addm_time,disch_time,'','','','','','','','','','']
        cur.execute( "INSERT INTO ADMISSIONS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ad_record)
        seqnum = -1
        for elem in row[4:]:
            seqnum += 1
            icd_record = [row[0],row[1],seqnum,icd_text(elem)]
            icd_records.append(icd_record)
cur.executemany('INSERT INTO DIAGNOSES_ICD VALUES (?,?,?,?)', icd_records)


cur.close()
conn.commit()
conn.close()