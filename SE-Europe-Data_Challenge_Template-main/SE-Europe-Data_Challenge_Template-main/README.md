# SE-Europe-Data_Challenge_Template
Template repository to work with for the NUWE - Schneider Electric European Data Science Challenge in November 2023.

# Tokens:
- b5b8c21b-a637-4e17-a8fe-0d39a16aa849
- fb81432a-3853-4c30-a105-117c86a433ca
- 2334f370-0c85-405e-bb90-c022445bd273
- 1d9cd4bd-f8aa-476c-8cc1-3442dc91506d

# 'C:/Users/pc/Desktop/podaci' is folder where all files are stored - after copy all necessary green energy type row_data.csv is generated

# Handle missing values
-Data for Germany, Hungary, Netherlands are at 15min resolution schould be aggregated into 1 hour intervals by summing every 4 consecutive rows  
-Data for UnitedKingdom are at 30min resolution schould be aggregated into 1 hour intervals by summing every 2 consecutive rows

# Cenerating new features
- df_processed['country_ID'] the idea is to make dictionary for each row of dataset. 
Key will be(0,1,2,3,4,5,6,7,8) {
SP: 0, # Spain
UK: 1, # United Kingdom
DE: 2, # Germany
DK: 3, # Denmark
HU: 5, # Hungary
SE: 4, # Sweden
IT: 6, # Italy
PO: 7, # Poland
NL: 8 # Netherlands
}
Value differece between green energy and load for each country.
Then get ID of country with maximum value and put it in variable ['country_ID'].
I created infinite for loop and I do not know to solve it.