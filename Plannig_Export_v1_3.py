import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import xlsxwriter
import numpy as np
import re


_names = 'panels, 09-04'

df = pd.read_excel('SW-Uygulama, AF, Panel Haftalık Yayın.xlsx', sheet_name=_names)

print("Column headings:")
print(df.columns)

#panel kodu -> df.columns[1]
#proje ismi -> df.columns[3]
#kabin kodu -> df.columns[4]
#...
#model_name -> df.columns[8]



'''
for i in df.index:
    print(df['Kabin Kodu'][i]) '''
print(df[df.columns[1]][0])
strpanel = df[df.columns[1]][0]

out = re.sub(r'\W+', '', strpanel)
out=str(out).upper()

out_basic = out[4:]
print(out,out_basic)

print(str(out_basic[2]).isalpha())

# -----
print(len(df[df.columns[1]]))
print("*"*100)

total_data = []
prior_data = []
_buf_prior = []
for i in range(len(df[df.columns[1]])):
    if str(re.sub(r'\W+', '', df[df.columns[3]][i]))=="AF":
        panel_raw = df[df.columns[1]][i]
        panel_clean = re.sub(r'\W+', '', panel_raw)
        panel_clean=panel_clean[4:] ; panel_clean=str(panel_clean).upper()
        priority = df[df.columns[0]][i] ### [priority] ###
        if panel_clean[-1].isalpha()==True: panel_clean=panel_clean[:-1]

        char_index=[]
        for n in range(len(panel_clean)):
            if panel_clean[n].isalpha()==True:
         #       print(panel_clean,panel_clean[n],end=" ")
                char_index.append(n)
        #print(char_index,end="#")

        _buf=panel_clean[:char_index[0]]
        if char_index[0]==2:
            _buf = '0' + _buf


        for ch in range(len(char_index)):
            _buf = _buf + str(panel_clean[char_index[ch]])


        _last =panel_clean[(char_index[-1]+1):]

        if len(_last)==2 and len(panel_clean)<6: _last = '0'+_last

        _buf = _buf + _last

        if len(_buf)<7: _buf = _buf[:-1] +'0'+_buf[-1]

        #print(_buf,end="*")
        _mn = []
        _cabin = str(df[df.columns[4]][i])
        _cab = _cabin.split(";")
        for c in range(len(_cab)):
            _cab[c] = str(re.sub(r'\W+', '', _cab[c]))
            _name = "Customer_A_"+ _buf + "_"+_cab[c]+"_0.ini"
            _mn.append(_name)

        #print(_mn,end=" ---> ")

        # lets write the package

        '''
        for ou in range(len(df.columns)):
            total_data.append(df[df.columns[ou]][i])
        '''
        total_data.append(_mn)

        prior_data.append([priority,_mn])
        _buf_mn = []
        _buf_mn.append(priority)
        for xx in range(len(_mn)):
            _buf_mn.append(_mn[xx])

        _buf_prior.append(_buf_mn)

        #print(total_data,end="\n")
    else:
        total_data.append   (False)



prior_data_2xN = []

for i in range (len(prior_data)):
    for j in range(len(prior_data[i][1])):
        #print(prior_data[i][0],prior_data[i][1][j])
        prior_data_2xN.append([prior_data[i][0],prior_data[i][1][j]])



print("*"*100)
print("prior_data")

print(len(prior_data))
for i in range (len(prior_data)):
    print(prior_data[i])

#lets unique......
a=np.array(prior_data_2xN)
a_uniq = np.unique(a, axis=0)
prior_data_uniq = a_uniq.copy()

print("*"*100)
print("prior_data_uniq")

print(len(prior_data_uniq))
for i in range (len(prior_data_uniq)):
    print(prior_data_uniq[i])


print("_-_"*100)
print("\n")

print(total_data[0])
print(prior_data[0])
print(_buf_prior[0])
print(prior_data_uniq[0])

print("\n")
print("_-_"*100)

##### prior_data manupulation
del prior_data
prior_data = _buf_prior.copy()
################################


df1 = pd.DataFrame(prior_data)
#df1.to_excel("output.xlsx",sheet_name='total')  # doctest: +SKIP
#------------------------------------
df2 = pd.DataFrame(prior_data_uniq)


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(_names+'.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
df1.to_excel(writer, sheet_name='total_list')
df2.to_excel(writer, sheet_name='unique')

# Close the Pandas Excel writer and output the Excel file.
writer.save()