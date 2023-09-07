I would like to show you a real example of an assignment I solved using Python

The company I worked for made machines that the customer could configure to suit their needs. 
Each of the parts of the machine (features) had several options, from which a client has to choose one. 
The company wanted to know which options for each feature in each type of machine were more likely to be selected than others. 
I was supposed to analyze the table of orders for the last 5 years. All the features selected by the client were indicated there for each order. 

__INPUT DATA: see an example "example_orders".__
Order - order number. Ordercode - code of the selected machine. 
The remaining columns list the features (the first letters in the name indicate the code of the machine they belong to).
<br />The selected option is written in the corresponding cell. 
<br />
<br /> __OUTPUT DATA: see an example "example_orders_output"__
<br />
<br />
<br />import pandas as pd
<br />import numpy as np
<br />
<br />pd.set_option('display.max_rows', None)
<br />pd.set_option('display.max_columns', None)
<br />pd.set_option('display.width', None)
<br />pd.set_option('display.max_colwidth', None)
<br />
<br />_#import data_
<br />df= pd.read_excel('example_orders.xlsx')
<br />
<br />_#enter machine model (here: ABC100)_
<br />df=df[df['ORDERCODE'].str.startswith('ABC100')]
<br /> 
<br /> _#enter machine code (here: ABC)_
<br /> df=df[df.columns[pd.Series(df.columns).str.startswith('ABC')]]
<br /> 
<br /> result2 = pd.DataFrame(columns=['Ordercode','Feature', 'Options', 'Count'])
<br /> _#a table to count all of the feature options_
<br /> result1 = pd.DataFrame(columns=['Feature1', 'Options1', 'Relative'])
<br /> _#a table to save the relative frequencies of the values_
<br /> result3 = pd.DataFrame(columns=['Feature', 'Options', 'Relative without `*`'])
<br /> _#a table to calculate the relative frequencies of the values excluding `*`_
<br /> result = pd.DataFrame(columns=['Ordercode','Feature', 'Options','Count','Relative','Relative without `*`'])
<br /> *#a table for the final result*
<br />
<br /> for column in df.columns:
<br />    
<br />   value_counts = df[column].value_counts()
<br />   *#value_counts() function returns object containing counts of unique values*
<br />   for idx, (value, count) in enumerate(value_counts.items()):
<br />     result2 = pd.concat([result2, pd.DataFrame({'Ordercode': a,'Feature': column, 'Options': value, 'Count': count}, index=[0])], ignore_index=True)
<br />       
<br /> value_counts = df[column].value_counts(normalize=True)
<br /> *#the function "value_counts(normalize=True)" returns the relative frequencies of the values*
<br /> for idx, (value, count) in enumerate(value_counts.items()):
<br />     result1 = pd.concat([result1, pd.DataFrame({'Feature1': column, 'Options1': value, 'Relative': count}, index=[0])], ignore_index=True) 
<br /> 
<br /> df1 = df.copy()
<br />       
<br /> for column in df1.columns:
<br />     df1[column] = df1[column].replace(['`*`'], None)
<br />     value_counts = (df1[column]).value_counts(normalize=True)
<br />    for idx, (value, count) in enumerate(value_counts.items()):
<br />      result3= pd.concat([result3, pd.DataFrame({'Feature': column, 'Options': value, 'Relative without `*`': count}, index=[0])], ignore_index=True)         
<br /> 
<br /> result3.loc[:, 'Relative without `*`'] = result3['Relative without *'].map('{:.2f}'.format)     
<br /> result33 = result3.replace(np.nan, '', regex=True)      
<br /> result = pd.concat([result2, result1], axis=1)     
<br /> result = pd.merge(result, result33, on=[ 'Feature', 'Options'], how="left")
<br /> result.loc[:, 'Relative'] = result['Relative'].map('{:.2f}'.format)
<br /> result=result.fillna("")
<br /> 
<br /> with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
<br />     print(result[['Ordercode','Feature', 'Options', 'Count', 'Relative','Relative without `*`']])
<br /> 
<br /> _#export data to excel_
<br /> with pd.ExcelWriter('Output.xlsx', mode='a', if_sheet_exists='overlay') as writer: 
<br /> _#change the name of the Excel sheet here if needed_
<br />     result[['Ordercode','Feature', 'Options', 'Count', 'Relative','Relative without `*`']].to_excel(writer, sheet_name='sheet1')
