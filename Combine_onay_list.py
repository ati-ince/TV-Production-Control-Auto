import os

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

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

'''
_filename = 'AF NX panel list 04092019 ver4'

df = pd.read_excel(_filename + '.xlsx')

xls = pd.ExcelFile(_filename + '.xlsx')

print(xls.sheet_names)
'''