import pandas as pd

#TODO: Scan all .xlsx files in the folder and appends them

df1 = pd.read_excel('Head Hanter_QA_2018-09-14 16-12-33.xlsx')
df2 = pd.read_excel('Head Hanter_automation_2018-09-14 16-12-36.xlsx')
df3 = df1.append(df2)
# df3.set_index('ID', inplace=True)
df4 = df3.drop_duplicates(subset=['ID'], keep='first')
df4.to_excel('Appended.xlsx',index=False)