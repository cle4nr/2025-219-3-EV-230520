import statistics as st
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
import datetime
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("test-299b9-firebase-adminsdk-73zi2-efd208c68f.json")
# cred = credentials.Certificate("C:/Users/ronan/OneDrive/Documents/GitHub/6thyearnew/!PROJECT/important files/test-299b9-firebase-adminsdk-73zi2-efd208c68f.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://test-299b9-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference('/allfighters')
fighters_dict = ref.get()


#function that gets their weight in kg and returns a value, which i can use to sort them into their weight divisions later
def weightcheck(weight):
    if weight != 'n/a':
        weight = int(weight)
        if weight > 94:
            return 8
        elif weight > 84:
            return 7
        elif weight > 78:
            return 6    
        elif weight > 71:
            return 5
        elif weight > 66:
            return 4
        elif weight > 62:
            return 3
        elif weight > 58:
            return 2
        else:
            return 1
        
#empty dictionaries for each weight class
flw=dict()
bw=dict()
fw=dict() 
lw=dict()
ww=dict()
mw=dict()
lhw=dict()
hw=dict()

#divisions dictionary and labels of divisions
divisions = {'flyweight':flw,'bantamweight':bw,'featherweight':fw,'lightweight':lw,'welterweight':ww,'middleweight':mw,'lightheavyweight':lhw,'heavyweight':hw}
mylabels = ['flyweight','bantamweight','featherweight','lightweight','welterweight','middleweight','lightheavyweight','heavyweight']

#this runs the function to return a value depending on their weight, and then sorts them into their weightclass dictionaries
for fighter,data in fighters_dict['Fighters'].items(): 
    weight = data.get("weight_in_kg") 
    if weight != '':  
        if weightcheck(weight) == 1:
            flw[fighter]=data
        if weightcheck(weight) == 2:
            bw[fighter]=data
        if weightcheck(weight) == 3:
            fw[fighter]=data
        if weightcheck(weight) == 4: 
            lw[fighter]=data 
        if weightcheck(weight) == 5:
            ww[fighter]=data
        if weightcheck(weight) == 6:
            mw[fighter]=data
        if weightcheck(weight) == 7:
            lhw[fighter]=data
        if weightcheck(weight) == 8:
            hw[fighter]=data

stances_dict = dict()
stancesall = dict()

#this for loop gets the amount of fighters with each stance in a divison, and saves it to a dictionary to be later displayed in a graph
for weightclass in divisions: 
    orth1, southpaw1, switch1 = 0,0,0 
    for fighter,data in divisions[weightclass].items(): 
        stance = data.get("stance") 
        if stance == "Orthodox": 
            orth1 += 1
        elif stance == "Southpaw":
            southpaw1+= 1
        elif stance == "Switch":
            switch1 += 1
    stancesall[weightclass] = {"orthodox":orth1,"southpaw":southpaw1,"switch":switch1}
    
#this displays the stances of each division onto a pie chart
#only did one weight class for this analysis, but in the website you will have the option to choose any weight class
piestances = input('piestances (y/n):') 
if piestances == 'y': 
    mylabels1 = ['Orthodox','Southpaw','Switch']
    y = np.array([stancesall['flyweight']['orthodox'],stancesall['flyweight']['southpaw'],stancesall['flyweight']['switch']])
    plt.pie(y, labels = mylabels1, autopct = '%.0f%%')
    plt.title('Flyweight stances') 
    plt.show() 

    
    
    
#this gets the average heights of each division and saves it to a list
avgheight = list()
for weightclass in divisions:
    templist=[]
    for fighter,data in divisions[weightclass].items():
        height = data.get("height_cm")
        if height != 'n/a':
            templist.append(height)
    meantemp = st.mean(templist)
    roundedmean = round(meantemp, 2)
    avgheight.append(roundedmean)


#this saves the average reaches into a list for all divisions
avgreach = list()
for weightclass in divisions:
    templist1=[]
    for fighter,data in divisions[weightclass].items():
        reach = data.get("reach_in_cm")
        if reach != 'n/a':
            templist1.append(reach)
    meantemp = st.mean(templist1)
    roundedmean = round(meantemp, 2)
    avgreach.append(roundedmean)
    
#this displays the average reach and height on a bar chart
reachheightavg = input('reach and height avg (y/n):')
if reachheightavg == 'y':
    
    xaxis= np.arange(len(mylabels)) 
    plt.bar(xaxis +0.2,avgheight,0.4,label='height')
    plt.bar(xaxis -0.2, avgreach,0.4,label='reach')
    
    plt.xticks(xaxis,mylabels) 
    plt.title('Average reach and height per weight class')
    plt.xlabel('Divisions')
    plt.ylabel('Reach and Height in cm')
    plt.legend(['height','reach'],loc="lower right")
    plt.show()
    
#this adds all the average ape indexes (reach / height) into a list
apeindexlist = list()
for x in range(len(divisions)):
    divape = avgreach[x] / avgheight[x]
    divape1 = round(divape, 2)
    apeindexlist.append(divape1)
 

#this graphs the fighter's average apeindex values on a bar chart and compares it to the average in humans which is 1
apeindex = input('apeindex (y/n):')
avgape = [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00]
if apeindex == 'y':

    xaxis2= np.arange(len(mylabels)) 
    plt.bar(xaxis2 +0.2,apeindexlist,0.4,label='apeindex')
    plt.bar(xaxis2 -0.2,avgape,0.4,label='avgape')
    
    plt.xticks(xaxis2,mylabels) 
    plt.title('Average ape index per weight class')
    plt.xlabel('Divisions')
    plt.ylabel('Ape index')
    plt.legend(['fighter avg','human avg'],loc="lower right")
    plt.show()
    


#this for loop adds the names of the fighters to a list to be used in the survey
fighters_list = []
for i in fighters_dict['Fighters']:
     fighters_list.append(i)


flwcount=0
bwcount=0
fwcount=0
lwcount=0
wwcount=0
mwcount=0
lhwcount=0
hwcount=0

#this for loop counts how many fighters are in each division and adds them to a dictionary for each division, to then be added to a list of all dictionaries
for x in divisions:
    for fighter, data in divisions[x].items():
        if x == 'flyweight':
            flwcount +=1
        if x == 'bantamweight':
            bwcount+=1
        if x == 'featherweight':
            fwcount+=1
        if x == 'lightweight':
            lwcount+=1
        if x == 'welterweight':
            wwcount+=1
        if x == 'middleweight':
            mwcount+=1
        if x == 'lightheavyweight':
            lhwcount+=1
        if x == 'heavyweight':
            hwcount+=1

countdiv = [flwcount,bwcount,fwcount,lwcount,wwcount,mwcount,lhwcount,hwcount]
#this displays the graph of the amount of fighters on a line chart
linecount = input('linecount (y/n):')
if linecount == 'y':
    plt.plot(mylabels,countdiv)
    plt.title('Amount of fighters in their respective weight class')
    plt.show() 






#this saves all the data gathered into a dictionary to be uploaded to firebase
analytics = dict()
analytics['Fighters per division'] = countdiv
analytics['Stances'] = stancesall
analytics['Heights'] = avgheight
analytics['Reaches'] = avgreach
analytics['Ape index']= apeindexlist
analytics['Fighter Names'] = fighters_list
ref = db.reference('/analytics')        
ref.set(analytics)            
            
    

