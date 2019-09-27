import os

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import numpy as np

import xlsxwriter
import numpy as np
import re

#get excel in directory -----------------------------------------------------------------------
# r=root, d=directories, f = files
_folder = os.getcwd()
latest= _folder.rfind('\\') #tersten elemean number
_folder=_folder[:latest]

_excel_cellonay_path='';_excel_panellist_path=''
def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

for file in files("../"):
    if str(file).split('.')[-1]=='xlsx':
        if 'cell' and 'onay' in str(file):
            _excel_cellonay_path=_folder+"\\"+str(file)
        elif 'panel' and 'list' in str(file):
            _excel_panellist_path=_folder+"\\"+str(file)
print(_excel_cellonay_path,'\n',_excel_panellist_path)
#----------------------------------------------------------------------------------------------

# // just now ... use only _excel_panellist_path

_file = _excel_panellist_path

xls = pd.ExcelFile(_file) # // with use panellist getting NX and AF....

print(xls.sheet_names)

df_panellist = [] #list

k=0
for i in xls.sheet_names:
    _buf = pd.read_excel(_file, sheet_name = i) # nex
    df_panellist.append(_buf)


_arr_af = df_panellist[1] #use [1] for AF
print(_arr_af)
_arr_af = np.asarray(_arr_af) #array yapısı kullanımı daha koaly durutor...
#----------------------------------
print(_arr_af[0])
print(_arr_af[1])