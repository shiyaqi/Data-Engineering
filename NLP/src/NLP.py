import json
import requests

api_key = "07d3c04d-14ce-42a3-8a5d-47e9585db48c"


def annotate(text):
    
    base_url = "http://data.bioontology.org"
    annotator_url = base_url + "/annotator"
    params = {"apikey": api_key,"format": "json","ontologies": "SNOMEDCT,LOINC", "text": text,
    }
    
    r = requests.get(annotator_url, params=params)
    
    result = r.json() 
    
    output_dict = {}
    
    if not text.strip():
        return output_dict
    else:
        for i in range(len(result)):
            key = result[i]["annotations"][0]["text"]
            value = result[i]["annotatedClass"]["@id"]
            if key in output_dict:
                output_dict[key].insert(-1,value)
            else:
                output_dict[key] = [value]   
    
        #return json.dumps(output_dict,indent=4,sort_keys=True) 
        return output_dict
    
    

sentence = """1.Hypertension. 2. Hypercholesterolemia. 3. Status post plastic surgery after a motor vehicle collision when he was in his 20s. 
#4. History of depression around the time of the accident. He does report that intermittently he feels quite down, but he is able "to pick himself back up". 
#More recently, however, he has been in a more prolonged period. 5. He has significant moles and he is followed by an outside dermatologist. 
#6. He has had normal PSA and rectal exams. He had a colonoscopy about five years ago and again one year ago, 
#both of which showed many polyps, pathology not known."""

print annotate(sentence)


