
# Importing the package that is necessary for us to be able to use the functionality for reading the csv file




import glob
from operator import contains 
import os
from xml.dom.minidom import Element
from numpy import False_
import pandas as pd
from array import *
import pip 

# This is the resource array that will store all the files data and we will access it one at a time
res=[]
headerSaver = list()
tempNumberIndex = 0
# This is to keep track of which file we are at and access that file
fileIndex=0
# This is a list of list that will store all the values in the fashion we want: for instance, timestamp, record, values, parameter etc.
multlist = [[],[],[],[],[],[],[]]
# This is the directory to access all the csv files in that directory 
dir_path =r'G:\ResearchLogNet\CAMnet\Stations & Data\Prince George Area\Ness Lake\Data\Tidy'
files  = glob.glob(dir_path+"\\*.xlsx")

#  Here we run a for loop from all the csv files found by python in that directory 
for filename in files:
    # this will fetch all the names of the excel files what we have in the particular folder
    tempName = os.path.splitext(os.path.basename(filename))[0]
     
    # this will read the file that are in excelFile
    read_file = pd.read_excel(filename)
    
    # now we convert the excel file that we recieved from excel file to same name excel file temporaily 
    read_file.to_csv(tempName+".csv", index = None, header =True)


    # # specifying the type of the csv file we will get
    df = pd.read_csv(tempName+".csv",encoding= 'unicode_escape', low_memory=False)
    # res. append the storing the file in an array 
    res.append(df)
    # This prints the filename and the index it is at
    print(filename)
    
    # to keep the track of what file we are at
                                                                                    # if the location is right file variable will open the .csv file and return it as an object Hence the dataFile
                         
    # Now we are accessing the file from that index and storing it into a datafile array
    dataFile = res[fileIndex]   
    fileIndex = fileIndex+1   
    # This is conditional check. Sometimes when we store the csv file from excel it saves extra commas which is needed to excluded (see NessLake_2013.csv for example ,,,,,,,, (like this))
    dataFile  = dataFile.loc[:,~dataFile.columns.str.contains('^Unnamed')]
    # Creating a variable of type array to store all the objects separately at different index

    # These are storing timeStamp and Record as they are going to be dublicated 
    
    Record  = list()
   
    # To keep track of how many columns we have in one file
    tempArrayLength = 0
    # goes to that file and run a loop to work with the contents inside the file
    for index, column in enumerate(dataFile):
    
        # save first column of file in a temparray
        tempArray = dataFile[column]
    
        # checks the name of column and save the values of that column in a TimeStamp array 
        if tempArray.name == "Timestamp":
        
            for myCol, x in enumerate(tempArray):
                TimeStamp = list()
                if myCol > 1:
                    TimeStamp.append(tempArray[myCol])
                    Record.append("null")
        # same here for record
        else: 
            if tempArray.name == "Record":
                 Record = list()
                 for myCol, x in enumerate(tempArray):
                    if myCol > 1:
                        Record.append(tempArray[myCol])

        
        # checks the name if not timestamp or record than it must be value 
        if tempArray.name != "Timestamp" and tempArray.name != "Record":
            #  to store identify what kind of values are they. These goes with values
            myValue=list()
            myUnitsId = list()
            myParam = list()
            myUnits = list()
            # checks if the length of the headerSaver is 0 which means there is no values in the head saver then go  to this loop and save that first name of the header saver
            if len(headerSaver)==0:
                
                headerSaver.append(tempArray.name)
                tempNumberIndex=1
            # In this loop we have a value found boolean vairable which is false initially 
            # In for loop for headSaver if head saver has a matching value with the tempArray Name then we will assgin it a number called tempNumnberIndex which would be saved
            # In the unitId
            else:  
                valueFound = False; 
                for range, nameIndex in enumerate(headerSaver):
                    
                    
                    if nameIndex == tempArray.name:
                        print(nameIndex,"=",tempArray.name)
                        tempNumberIndex = range+1
                        valueFound = True
                        break
                    tempNumberIndex = range+1
                    
                #Now if the value was found in that for loop then this should be true else we will save that value in our header and assign that a tempnumber as well     
                if valueFound ==True:
                    
                    valueFound = False
                else:
                    headerSaver.append(tempArray.name)
                    
            for myCol, x in enumerate(tempArray):
            
                if myCol > 1:
                    multlist[2].append(tempArray[myCol])      
                    multlist[3].append(tempNumberIndex)
                    multlist[4].append(tempArray.name)
                    multlist[5].append(tempArray[0])
                
        tempArrayLength = index;
        print (index)

    i =1;
    while i < tempArrayLength:
        multlist[0].extend(TimeStamp)
        multlist[1].extend(Record) 
        i=i+1




dict = {"TimeStamp": multlist[0], "Record": multlist[1],"Value": multlist[2], "Parameter": multlist[3], "Units_ID":multlist[4],"Units":multlist[5], }

df = pd.DataFrame(dict)
df.to_csv("result/result.csv")

print("The transfer was successful have a good day or not... who cares as long as the transfer was successful")
# result id unknown
# qaqc for the highlighted one 
