I would like to show you a real example of an assignment I solved using Python

The company I worked for made machines that the customer could configure to suit their needs. 
Each of the parts of the machine (features) had several options, from which a client has to choose one. 
The company wanted to know which options for each feature in each type of machine were more likely to be selected than others. 
I was supposed to analyze the table of orders for the last 5 years. All the features selected by the client were indicated there for each order. 

INPUT DATA: see an example "example_orders".
Order - order number. 
Ordercode - code of the selected machine. 
The remaining columns list the features (the first letters in the name indicate the code of the machine they belong to).
The selected option is written in the corresponding cell. 

OUTPUT DATA: see an example "example_orders_output"

                                                                                                                                
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

  #import data:
df= pd.read_excel('example_orders.xlsx')

  #enter machine model (here: ABC100):
df=df[df['ORDERCODE'].str.startswith('ABC100')]

  #enter machine code (here: ABC):
df=df[df.columns[pd.Series(df.columns).str.startswith('ABC')]]
 
result2 = pd.DataFrame(columns=['Ordercode','Feature', 'Options', 'Count'])
      #a table to count all of the feature options
result1 = pd.DataFrame(columns=['Feature1', 'Options1', 'Relative'])
      #a table to save the relative frequencies of the values
result3 = pd.DataFrame(columns=['Feature', 'Options', 'Relative without *'])
      #a table to calculate the relative frequencies of the values excluding *
result = pd.DataFrame(columns=['Ordercode','Feature', 'Options','Count','Relative','Relative without *'])
      #a table for the final result

for column in df.columns:
      value_counts = df[column].value_counts()
      #value_counts() function returns object containing counts of unique values
      for idx, (value, count) in enumerate(value_counts.items()):
          result2 = pd.concat([result2, pd.DataFrame({'Ordercode': a,'Feature': column, 'Options': value, 'Count': count}, index=[0])], ignore_index=True)
       
      value_counts = df[column].value_counts(normalize=True)
      #the function "value_counts(normalize=True)" returns the relative frequencies of the values
      for idx, (value, count) in enumerate(value_counts.items()):
          result1 = pd.concat([result1, pd.DataFrame({'Feature1': column, 'Options1': value, 'Relative': count}, index=[0])], ignore_index=True) 
 
df1 = df.copy()
       
for column in df1.columns:
   df1[column] = df1[column].replace(['`*`'], None)
   value_counts = (df1[column]).value_counts(normalize=True)
   for idx, (value, count) in enumerate(value_counts.items()):
               result3= pd.concat([result3, pd.DataFrame({'Feature': column, 'Options': value, 'Relative without *': count}, index=[0])], ignore_index=True)         
 
result3.loc[:, 'Relative without *'] = result3['Relative without *'].map('{:.2f}'.format)     
result33 = result3.replace(np.nan, '', regex=True)      
result = pd.concat([result2, result1], axis=1)     
result = pd.merge(result, result33, on=[ 'Feature', 'Options'], how="left")
result.loc[:, 'Relative'] = result['Relative'].map('{:.2f}'.format)
result=result.fillna("")
 
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
      print(result[['Ordercode','Feature', 'Options', 'Count', 'Relative','Relative without *']])
 
#export data to excel:
with pd.ExcelWriter('Output.xlsx', mode='a', if_sheet_exists='overlay') as writer:
      #change the name of the Excel sheet here if needed
      result[['Ordercode','Feature', 'Options', 'Count', 'Relative','Relative without `*`']].to_excel(writer, sheet_name='sheet1')
