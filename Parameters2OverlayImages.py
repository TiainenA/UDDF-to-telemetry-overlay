import os
from PIL import Image, ImageDraw, ImageFont
from UDDF_telemetry import UDDF_Reader,ParameterReader
import matplotlib.colors



def kuvain(Parameters,DiveInfo, UsedColumns, DFSlice):
    #A in RGBA is the opacity (why it isn't RGBO?)
    image = Image.new("RGBA", (int(Parameters["ResolutionX"]), int(Parameters["ResolutionY"])), (255, 255, 255, 0))
   


    font = ImageFont.truetype("arial.ttf", int(Parameters["FontSize"]))

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)
    #This goes through the parameters and draws them to the screen one by one
    for column in UsedColumns:
        if column == "alarm" and str(DFSlice[Parameters[column+"Variable"]])=="nan":
            continue
        if column == "tankpressure":
            Variable=int(DFSlice[Parameters[column+"Variable"]])/10000
            unit=Parameters[column+"Unit"]
        elif column == "temperature":
            Variable=int(DFSlice[Parameters[column+"Variable"]])-273
            unit= '\xb0 C'
        else:
            Variable=DFSlice[Parameters[column+"Variable"]]
            unit=Parameters[column+"Unit"]
        #Determining text, location, and color
        text = f"{Parameters[column+"Text"]} {Variable} {unit}"
        
        x = int(Parameters[column+"X"])/100*int(Parameters["ResolutionX"])
        y = int(Parameters[column+"Y"])/100*int(Parameters["ResolutionY"])


        textColor=matplotlib.colors.to_rgba_array(Parameters[column+"Color"])[0].tolist()
        
        textOpacity=255*int(Parameters[column+"Opacity"])


        for i in range(len(textColor)):
            textColor[i-1]=255*int(textColor[i-1])

        draw.text((x, y), text, font=font, fill=(textColor[0], textColor[1], textColor[2], textOpacity))
    
    filename=f"{DiveInfo["datetime"].replace(":","")}"
    image.save(f"{os.getcwd()+Parameters.get("OutputPath")}\\{filename}_DT_{DFSlice['ns1:divetime']}.png") 


def main():
    BasicParameters = ParameterReader()
    DiveData,DiveInfo,InterestingParameters=UDDF_Reader()
    for index,row in DiveData.iterrows():
        #print(row['ns1:divetime'], row['ns1:depth'],row['ns1:alarm'])
        kuvain(BasicParameters, DiveInfo, InterestingParameters, row)   

if __name__ == "__main__":
    main()
 