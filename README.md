# Data-Engineering
CSV_JSON/CSV_XML : 
Converted data from CSV to JSON and XML in Python

Parse_HL7_Msg/NoSQL : 
Parsed HL7 messages using the HL7apy Library in Python. 
Process and structure the data with UMLS concepts and JSON-LD
Saved the JSON-LD document to MongoDB 

NLP: 
Wrote functions that receive a string of unstructured text
Send the text to Bioportal REST service
Get the results(structured data) in JSON
Parsed the results.

ETL/SQL:
Read CSV files 
Performed ETL
populated the appropriate columns into tables.
Stored tables into relational database.
Queried the database in SQL to answer questions such as: 
1. What are the admission ID's of patients with a diagnosis of "Asthma, Exercise Induced"?
2. What are the admission ID's of patients with a diagnosis of "Asthma, Exercise Induced" as the primary diagnosis?
3. How many admissions were there where "Emphysema" was a primary diagnosis?
4. How many admissions were there where "Emphysema" was a secondary diagnosis?
5. How many admissions were there where "Emphysema" was one of the first 3 diagnoses?
6. How many patients were there where "COPD, NOS" was one of the diagnosis codes?
7. What are the lengths of stay for all admissions?
8. What are the lengths of stay for all admissions involving "COPD, NOS"?
9. What is the average length of stay for all admissions?
10. What is the average length of stay for all admissions involving "Heart failure, combined, unspecified"?
11. How many patients have more than 1 admission?
12. Of those patients with more than 1 admission, what is the average number of admissions?

ML/SVM:
utilize numpy, sci-kit learn and matplotlib to train and test a support vector machine (SVM) to detect diabetes using the diabetes data set from the UC Irvine machine learning repository. 
