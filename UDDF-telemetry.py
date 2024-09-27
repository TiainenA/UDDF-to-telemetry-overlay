import os
#
# from pyautogui import typewrite

#import shutil
import pandas as pd
import csv
import UDDF_CSV_Reader



def ParameterReader():
    with open("Parameters.csv", mode='r') as file:
        reader = csv.reader(file)
        mydict = {rows[0]:rows[1] for rows in reader}
    return(mydict)

def main():
    Parameters=ParameterReader()
    x=Parameters.get("DefaultFolder")
    Parameters["Folder"]= input(f"Type non-default folder or leave empty as default value of  {x}")
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
    print(FileList[FileNumber])


    df=UDDF_CSV_Reader.TelemetryReader(path+FileList[FileNumber])

    #print(df.to_string())
 

  

if __name__ == "__main__":
    main()

