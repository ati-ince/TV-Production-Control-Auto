import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import xlsxwriter
import numpy as np
import codecs
import re

# ----------------------------------------------------------------------------------------------
_filelink= "\\\\arcei34v\\SOFTWARE\\SERI\\AF\\Model_Names.ini"
f = open(_filelink)
# ----------------------------------------------------------------------------------------------
_file = f.read()
f.close()

with open(_filelink) as f:
    lines = f.readlines()

print(len(lines))

for i in lines:
    print(i[:-1])




# // \\arcei34v\SOFTWARE\SERI\AF\Model_Names.ini