import argparse
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timezone


def load_data(file_path):
    # Load data from CSV file

    df = pd.read_csv(file_path, delimiter=',', engine='python') # here the given csv file is reading

    return df

def clean_data(df):
    # TODO: Handle missing values, outliers, etc.

    df_clean = df.fillna(0) # replace Nan to 0
   
    
    
    #Data for Germany, Hungary, Netherlands are at 15min resolution schould be aggregated into 1 hour intervals by summing every 4 consecutive rows  
    #Data for UnitedKingdom are at 30min resolution schould be aggregated into 1 hour intervals by summing every 2 consecutive rows
    
    N=4   #number of consecutive rows for Germany, Hungary and Netherlands
    M=2   #number of consecutive rows for UK
    #first remove last rows if remainders
    df_clean = df_clean.iloc[:len(df_clean) // N * N]
    #convert to numeric 
    df_clean.loc[:,('green_energy_DE')] = pd.to_numeric(df_clean['green_energy_DE'], errors='coerce').fillna(0).astype(int)
    df_clean.loc[:,('green_energy_HU')] = pd.to_numeric(df_clean['green_energy_HU'], errors='coerce').fillna(0).astype(int)
    df_clean.loc[:,('green_energy_NE')] = pd.to_numeric(df_clean['green_energy_NE'], errors='coerce').fillna(0).astype(int)
    df_clean.loc[:,('green_energy_UK')] = pd.to_numeric(df_clean['green_energy_UK'], errors='coerce').fillna(0).astype(int)
    df_clean.loc[:,('DE_Load')] = pd.to_numeric(df_clean['DE_Load'], errors='coerce').fillna(0).astype(int)
    df_clean.loc[:,('HU_Load')] = pd.to_numeric(df_clean['HU_Load'], errors='coerce').fillna(0).astype(int)
    df_clean.loc[:,('NE_Load')] = pd.to_numeric(df_clean['NE_Load'], errors='coerce').fillna(0).astype(int)
    df_clean.loc[:,('UK_Load')] = pd.to_numeric(df_clean['UK_Load'], errors='coerce').fillna(0).astype(int)
   
    #aggregate sum 
    df_clean.loc[:,('green_energy_DE')] = df_clean['green_energy_DE'].shift(-N).rolling(N, min_periods=1).sum() 
    df_clean.loc[:,('green_energy_HU')] = df_clean['green_energy_HU'].shift(-N).rolling(N, min_periods=1).sum() 
    df_clean.loc[:,('green_energy_NE')] = df_clean['green_energy_NE'].shift(-N).rolling(N, min_periods=1).sum() 
    df_clean.loc[:,('green_energy_UK')] = df_clean['green_energy_UK'].shift(-M).rolling(M, min_periods=1).sum() 
    df_clean.loc[:,('DE_Load')] = df_clean['DE_Load'].shift(-N).rolling(N, min_periods=1).sum()
    df_clean.loc[:,('HU_Load')] = df_clean['HU_Load'].shift(-N).rolling(N, min_periods=1).sum()
    df_clean.loc[:,('NE_Load')] = df_clean['NE_Load'].shift(-N).rolling(N, min_periods=1).sum()
    df_clean.loc[:,('UK_Load')] = df_clean['UK_Load'].shift(-N).rolling(N, min_periods=1).sum()
    
   # df_clean.index = pd.to_datetime(df_clean.index) 

   # df_clean.resample('H').mean() #  taking the mean of the top and bottom value of the missing value
   # df_clean.interpolate() do not know to solve error which I get
    

    return df_clean

def preprocess_data(df):
    # TODO: Generate new features, transform existing features, resampling, etc.
    
    #df['datetime'] = datetime.fromisoformat('datetime'[:-1]).astimezone(timezone.utc)
    #df['datetime']=df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    #df.groupby(pd.Grouper(key='datetime', freq='H')).sum() #transform existing features by summarized rows with same datetime
    
    df_processed = df
    
    dict = {}
    for i in df.index:
       
        key1 =input(0) #Spain
        value1 = input(df['SP_Load'][i] - df['green_energy_DE'][i] )
        dict[key1] = value1
        key2 =input('1') #United Kindom
        value2 = input(df['UK_Load'][i] - df['green_energy_UK'][i] )
        dict[key2] = value2
        key3 =input('2') #Germany
        value3 = input(df['DE_Load'][i] - df['green_energy_DE'][i] )
        dict[key3] = value3
        key4 =input('3') #Denmark
        value4 = input(df['DK_Load'][i] - df['green_energy_DK'][i] )
        dict[key4] = value4
        key5 =input('4') #Hungary
        value5 = input(df['HU_Load'][i] - df['green_energy_HU'][i] )
        dict[key5] = value5
        key6 =input('5') #Sweden
        value6 = input(df['SE_Load'][i] - df['green_energy_SE'][i] )
        dict[key6] = value6
        key7 =input('6') #Italy
        value7 = input(df['IT_Load'][i] - df['green_energy_IT'][i] )
        dict[key7] = value7
        key8 =input('7') #Poland
        value8 = input(df['PO_Load'][i] - df['green_energy_PO'][i] )
        dict[key8] = value8
        key9 =input('8') #NEtherlands
        value9 = input(df['NE_Load'][i] - df['green_energy_NE'][i] )
        dict[key9] = value9
        res = {key : sorted(val, key = lambda ele : (ele[0], ele[1]))[-1] for key, val in dict.items()} #return max element in dictionary
        
        df_processed['country_ID'] = res

    print(df_processed.head(4))

    return df_processed

def save_data(df, output_file):
    # Save the dataframe to a CSV file
 #   df.to_csv('my_train.csv', encoding='utf-8')
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Data processing script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file',
        type=str,
        default=r'C:\Users\pc\Desktop\row_data.csv',
        help='Path to the raw data file to process'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='data/processed_data.csv', 
        help='Path to save the processed data'
    )
    return parser.parse_args()

def main(input_file, output_file):
    df = load_data(input_file)
    df_clean = clean_data(df)
    df_processed = preprocess_data(df_clean)
    save_data(df_processed, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)