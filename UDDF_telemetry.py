import os
from datetime import datetime

import pandas as pd
import csv
import UDDF_CSV_Reader
import Parameters2OverlayImages


def ParameterReader():
    with open("Parameters.csv", mode='r') as file:
        reader = csv.reader(file)
        mydict = {rows[0]:rows[1] for rows in reader}
    return(mydict)

def UDDF_Reader():

    #To get all parameters in the settings
    Parameters=ParameterReader()
    DiveInfo={}

    UsedParams=[]
    for key in Parameters:
        if Parameters[key]=="TRUE":
            UsedParams.append(key)
    #To get the parameter variable names
    ParamVariables=[]
    for key in UsedParams:
        ParamVariables.append(Parameters.get(key+"Variable"))
   

    
    InputVar=Parameters.get("DefaultFolder")

    Parameters["Folder"]= input(f"Type non-default folder or leave empty as default value of  {InputVar}")
    
    
    if Parameters.get("Folder")=="":
        Parameters["Folder"]=os.getcwd()+Parameters.get("DefaultFolder")

    path=Parameters.get("Folder")



    FileList=[]
    for (file) in os.listdir(path):
            if file.endswith('.csv'):
                print(f"[{len(FileList)}] {file}")
                FileList.append(file)
    
    FileNumber= input(f"Which file is processed or leave empty as default value of [0]")

    if FileNumber=="":
         FileNumber=0
    else:
        FileNumber=int(FileNumber)    
    
    print(path+FileList[FileNumber])


    df=UDDF_CSV_Reader.TelemetryReader(path+FileList[FileNumber])
    
    #Set Dive info, such as date and location
    DiveInfoKeys=['datetime','location','latitude','longitude']
    DiveInfoColumns=['ns1:datetime','ns1:name12','ns1:latitude','ns1:longitude']
    for i in range(len(DiveInfoKeys)):

        if DiveInfoColumns[i-1] in df.columns.tolist():
             DiveInfo[DiveInfoKeys[i-1]]=df[DiveInfoColumns[i-1]].iloc[0]

    #To convert the time format
    
    DiveInfo["datetimeISO"] = datetime.strptime(DiveInfo["datetime"], "%d.%m.%Y %H:%M").isoformat()
    
    
    #Forward filling option 
    if Parameters.get("MissingValues")=="ffill":
        #df=df.ffill(limit=50)
        df=df.interpolate()
        
    #Removing NAN values in ns1:divetime from the beginning
    df = df[df['ns1:divetime'].notna()]
    #Removes unusable parameters from that particular dive (for example if no air integration and it was desired)
    RemovedVariables=[]
    for i in UsedParams:
        if Parameters[i+"Variable"] in df.columns.tolist():
            continue
        else:
            RemovedVariables.append(i)
    if len(RemovedVariables) != 0:
        for i in RemovedVariables:
            UsedParams.remove(i)
        print(f"Removed following parameters {RemovedVariables}")


    #Dropping all other variables
    FilteredDF=df.filter(ParamVariables,axis=1)

    return(FilteredDF, DiveInfo,UsedParams)    



def main():
    BasicParameters = ParameterReader()
    DiveData,DiveInfo,InterestingParameters=UDDF_Reader()
    for index,row in DiveData.iterrows():
        #print(row['ns1:divetime'], row['ns1:depth'],row['ns1:alarm'])
        Parameters2OverlayImages.kuvain(BasicParameters, DiveInfo, InterestingParameters, row)  
if __name__ == "__main__":
    main()

