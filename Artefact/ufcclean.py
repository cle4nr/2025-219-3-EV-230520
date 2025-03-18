import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("test-299b9-firebase-adminsdk-73zi2-efd208c68f.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://test-299b9-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference('/')

#function that takes a value and attempts to turn it into an int or a float, if it is not a number it ignores
def convert_value(value):
    try:
        value = int(value)                           
    except ValueError:   5
    try:
        value = float(value) 
    except ValueError:
        pass
    return value


with open("ufc-fighters-statistics_all.csv") as data_file: 
    headersstring = data_file.readline().strip("\n") 
    headers = headersstring.split(",")[1:] 
    fighters_dict = dict() 
    
    #this for loop cleans the data and sorts it into a dictionary after cleaning. it converts the strings with digits into floats and ints
    #it also removes illegal characters so it can be uploaded to firebase
    for line in data_file:
        name, data = line.strip().split(",", maxsplit=1) 

        values = list() 
        for value in data.split(","): 
            values.append(convert_value(value)) 
        if '.' in name: 
            name = name.replace('.','') 
        if "'" in name: 
            name = name.replace("'","")
            
        fighters_dict[name] = {headers[i]:values[i] for i in range(len(values))}
    #this for loop takes whitespace and replaces it with n/a
    for fighter,data in fighters_dict.items(): 
        for v in data: 
            if data[v] == '': 
                data[v] = 'n/a' 
allfighters = dict() 
allfighters['Fighters'] = fighters_dict #i added the dictionary of fighters, to an extra dictionary so that it has its own subheading in firebase

ref = db.reference('/allfighters')  
ref.set(allfighters)
        