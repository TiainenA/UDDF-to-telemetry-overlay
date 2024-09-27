import pandas as pd
import csv

def TelemetryReader(filepath:str):
    df = pd.read_csv(filepath, sep=';')
    return(df)


def main():
    
    
    path='Data\\2024-09-22 Dive1.csv'
    data = TelemetryReader(path)

    first_10_rows = data.head(10) 
    print(first_10_rows)
if __name__ == "__main__":
    main()
