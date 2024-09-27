import os
#from pyautogui import typewrite
import pandas as pd
import csv
import UDDF_CSV_Reader



def ParameterReader():
    with open("Parameters.csv", mode='r') as file:
        reader = csv.reader(file)
        mydict = {rows[0]:rows[1] for rows in reader}
    return(mydict)

def main():
    #To get all parameters in the settings
    Parameters=ParameterReader()
    UsedParams=[]
    for key in Parameters:
        if Parameters[key]=="TRUE":
            UsedParams.append(key)
    #To get the parameter variable names
    ParamVariables=[]
    for key in UsedParams:
        ParamVariables.append(Parameters.get(key+"Variable"))



    #df = pd.read_csv("C:\\Users\\User\\github\\UDDF-to-telemetry-overlay\\Data\\2024-09-22 Dive1.csv", sep=';')



    

    
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
    #Forward filling option 
    if Parameters.get("MissingValues")=="ffill":
        df=df.ffill(limit=50)

    #Dropping all other variables
    FilteredDF=df.filter(ParamVariables,axis=1)
  

if __name__ == "__main__":
    main()

