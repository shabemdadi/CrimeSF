import requests
import json

#import data from BJS as JSON file(saved output JSON file to comp because takes too long to request each time)

# file = requests.get("http://www.bjs.gov:8080/bjs/ncvs/v2/personal/2013?format=json")
# text_format = file.text

file = open("NCVS_2013_PERSONAL.json")
text = file.read()
text_read = json.loads(text)

#designate desired fields
victim_info_dict = text_read["personalData"]
variables = text_read["personalData"][0].keys()
variables_dict = ['ethnic1', 'weight', 'locationr', 'newoff', 'race1', 'notify', 'year', 'direl', 'marital2', 'treatment', 'hincome', 'injury', 
            'msa', 'vicservices', 'ethnic', 'newcrime', 'weapon', 'gender', 'age', 'popsize', 'hispanic', 'race', 'seriousviolent', 'region', 
            'weapcat']

rename_inputs_dict = {'age':{'1':(12,14),'2':(15,17),'3':(18,20),'4':(21,24),'5':(25,34),'6':(35,49),'7':(50,64),'8':(65,100)},
                      'gender':{'1':'Male','2':'Female'},
                      'seriousviolent':{'1':'Serious Violent', '2':'Simple Assault','3':'Personal Theft','4':'Property Crime'}}

#use dictionary to rename dummy variables
for victim_data in victim_info_dict:                    #iterate through rows of data, each row is a dictionary
    for variable in victim_data:                        #iterate through each key in each row of dictionary
        if variable in rename_inputs_dict:              #if variable is within our rename_inputs dictionary, rename the value to the one we have designated
            if victim_data[variable] in rename_inputs_dict[variable]:
                victim_data[variable] = rename_inputs_dict[variable][victim_data[variable]]

# testing                
print text_read.keys()
print text_read["personalData"][0].keys() # shows variables in data
print text_read["personalData"][0]["age"]
print text_read["personalData"][0]["gender"]
print text_read["personalData"][0]["seriousviolent"]

