# legacy from app1_3 ........
#legacy from ProductionAnalysis_Report_v2_3

'''
How to use.......

TV üretim excel'ine yeni sheet olarak Emre tablo giriyoruz...
Yazılım buradan çekerek kullanmakta....

Bu şasi planı için

-> buna model_Name.ini oto üretme mekanizması ekliyorum.


'''

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import xlsxwriter
import numpy as np
import codecs
import re
#######################3
import sys
#print(sys.path)
#sys.path.append('D:\\#PyProjects\\#modules-libraries-functions\\my-precious-shared')
#print(sys.path)



_file = '../sası_planı_16.09.2019' #bir ust dizinden almakta....
_filename = _file +'.xlsx'
_sheet_name = 'Sıralama'

_sheet_model = 'unique_list'

_export_report_name = _file + '-' +  _sheet_model + '-' + 'SW_Model_ONAY_KONTROL'

df = pd.read_excel(_filename, sheet_name=_sheet_name)

print("Column headings:")
print(df.columns)

''' df['Kabin Kodu'][i] '''
# neler kullanacağız.....
# [0] df['Tarih']   -> üretim tarihi [0]
# [4] df['Malzeme110']   -> şasi kodu....  [4]
# [6] df['BMS']  -> 56 'lı panel kodu.... [6]
# [9] df['Sasi']   -> şasi kodu AF NX vb....  [9]
# [10] df['Mamul']   -> Mamul kodu 000'lı  [10]
# [11] df['  Miktar']  ->  üretim miktarı... [11]
# [12] df['Ön Çerçeve']  -> kabin bilgimiz (Kabin:Açıklama).... [12]
# ----------------------------------------------------------------------------------------------


# test the numbers ..............................................
print(len(df['Malzeme110']),df['Malzeme110'][0])
print(len(df[df.columns[4]]),df[df.columns[4]][0])
print("*"*100);print("*"*100)

# AF'leri ayıklayalım 'AF' yada 'AF:xxxx' gelmekte ; #ref olarak şasi alalım
# ----------------------------------------------------------------------------------------------
def modelname_create(panel, kabin):
    if panel != 'nan':  # af_list[i][2]
        panel_raw = panel #af_list[i][2]
        panel_clean = re.sub(r'\W+', '', panel_raw)
        panel_clean = panel_clean[4:];
        panel_clean = str(panel_clean).upper()

        if panel_clean[-1].isalpha() == True: panel_clean = panel_clean[:-1]

        char_index = []
        for n in range(len(panel_clean)):
            if panel_clean[n].isalpha() == True:
                #       print(panel_clean,panel_clean[n],end=" ")
                char_index.append(n)
        # print(char_index,end="#")

        _buf = panel_clean[:char_index[0]]
        if char_index[0] == 2:
            _buf = '0' + _buf

        for ch in range(len(char_index)):
            _buf = _buf + str(panel_clean[char_index[ch]])

        _last = panel_clean[(char_index[-1] + 1):]

        if len(_last) == 2 and len(panel_clean) < 6: _last = '0' + _last

        _buf = _buf + _last

        if len(_buf) < 7: _buf = _buf[:-1] + '0' + _buf[-1]

        _pan = _buf
        _cab = kabin  # af_list[i][4];
        _cab = str(re.sub(r'\W+', '', _cab))
        _name = "Customer_A_" + _pan + "_" + _cab + "_0.ini"

        return _name
    else:
        return 'ERROR_PANEL_NAME'
# ----------------------------------------------------------------------------------------------
df_sw = pd.read_excel(_filename, sheet_name=_sheet_model)

print("Column headings:")
print(df_sw.columns)

''' df['Unique Model_Name''][i] '''
# neler kullanacağız.....
# [2] df['Unique Model_Name'']   -> model_name  [2]
# [3] df['AF - SW Build']  -> sw release   [3]

print('total_len',len(df_sw[df_sw.columns[2]]))
sw_model_list=[]
for i in range(len(df_sw[df_sw.columns[2]])):
    _mod = df_sw[df_sw.columns[2]][i]
    _sw_raw= str (df_sw[df_sw.columns[3]][i])
    if _sw_raw == 'nan': _sw_raw = 'Waiting_SW_Relese_Code'
    sw_model_list.append([_mod,_sw_raw])

print('basarılı ..... unique... ')

def sw_model_check(_model , _inlist):
    _out = 'MODEL_NOT_IN_SW_RELEASE'
    index=0
    for j in range(len(_inlist)):
        if _model in _inlist[j]:
            _out = _inlist[j][1] # 0 ise model name , 1 is sw_release
            break
    return _out

# ----------------------------------------------------------------------------------------------
f = codecs.open('../' + 'Model_Names' +'.ini',"w+", encoding='utf-8')
# ----------------------------------------------------------------------------------------------

f.write("### Used with "+ _file+" ###\n")
f.write("[AFMODELNAME]\n")

af_list = []
for i in range(len(df[df.columns[0]])):
    _buf_sasi= str(df[df.columns[9]][i]).split(':')[0]
    if _buf_sasi == 'AF':
        _tarih=str(df[df.columns[0]][i])
        _sasi110=str(df[df.columns[4]][i])
        _bms56panel= str(df[df.columns[6]][i]) #bazıları kodu verilmemiş ???? elle verdik ayarlayacagız...
        _sasi = str(df[df.columns[9]][i]).split(':')[0]
        _mamul = str(df[df.columns[10]][i])
        _miktar = str(df[df.columns[11]][i])
        _kabin = str(df[df.columns[12]][i]).split(':')[0]
        _model_name = modelname_create(_bms56panel, _kabin)
        _sw_info = str(sw_model_check(_model_name , sw_model_list))
        _onay = 'OK'
        if _sw_info== 'MODEL_NOT_IN_SW_RELEASE': _onay = 'NOK'
        elif 'Greta' or 'Clara' in _sw_info: _onay='OK'
        else: _onay='!Waiting_to_ADD!'
        af_list.append([_tarih,_sasi,_mamul,_sasi110,_bms56panel,_kabin,_miktar,_model_name,_sw_info,_onay])
        ## write to check data
        f.write("%s=%s\n" %(_sasi110[:3],_model_name))

strTarih = 'Üretim Tarih'
strSasi = 'Şasi'
strMamul = 'Mamul'
strSasi110 = 'Şasi110'
strBMS56panel = 'BMS56panel'
strKabin = 'Kabin'
strMiktar = 'Miktar'
strModel_Name = 'Model_Name'
strSW_Info = 'SW_Info'
strUretim_Onayı = 'Uretim_Onayı'


for i in range(len(af_list)):
    #if 'nan' in af_list[i]:
    print(i,"#",af_list[i])
 #yazdır son halini, af_list....

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

df1 = pd.DataFrame(af_list)
writer = pd.ExcelWriter(_export_report_name+'.xlsx', engine='xlsxwriter')

#header
df1.columns = [strTarih,strSasi,strMamul,strSasi110,strBMS56panel,strKabin,strMiktar,strModel_Name,strSW_Info,strUretim_Onayı]

# Write each dataframe to a different worksheet.
df1.to_excel(writer, sheet_name='onay_durum')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

# close the file
f.close()