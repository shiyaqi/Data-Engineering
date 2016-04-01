SELECT hadm_id FROM diagnoses_icd WHERE icd9_code = '493.81';
SELECT hadm_id FROM diagnoses_icd WHERE sequence = 0 AND icd9_code = '493.81';
SELECT count(*) From diagnoses_icd WHERE sequence = 0 AND icd9_code like '492%';
SELECT count(*) From diagnoses_icd WHERE sequence = 1 AND icd9_code like '492%';
SELECT count(*) From diagnoses_icd WHERE sequence>=0 and sequence<= 2 AND icd9_code like '492%';
SELECT count(*) FROM (SELECT DISTINCT subject_id FROM diagnoses_icd WHERE icd9_code LIKE'496%');
SELECT julianday(dischtime) - julianday(admittime) FROM admissions;
SELECT JULIANDAY(dischtime)- JULIANDAY(admittime) FROM diagnoses_icd JOIN admissions ON diagnoses_icd.hadm_id = admissions.hadm_id WHERE icd9_code LIKE '496%';
SELECT avg(julianday(dischtime) - julianday(admittime)) FROM admissions;
SELECT avg(JULIANDAY(dischtime)- JULIANDAY(admittime)) FROM diagnoses_icd JOIN admissions ON diagnoses_icd.hadm_id = admissions.hadm_id WHERE icd9_code= '428.40';
SELECT count(*) FROM (SELECT count(*) FROM admissions GROUP BY subject_id HAVING count(*)>1);
SELECT avg(admnum) FROM (SELECT count(*) as admnum FROM admissions GROUP BY subject_id HAVING count(*)>1);





