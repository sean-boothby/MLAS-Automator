# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 15:19:21 2018

@author: sean
"""

## Feed this script any folder filled with xlsx files of a similar nature and they will be joined together into one dataframe

import os
import yaml
import subprocess
import pandas as pd


config = yaml.safe_load(open("config/config.yml"))
dlPath = config['downloads']['downloadpath']

def pandasConcat(path):
    xlsxFiles = []
#    masterdf=pd.DataFrame()
    Files = os.listdir(path)
    for file in Files:
        if '.xlsx' in file:
            xlsxFiles.append(file)
    for index, xlsFile in enumerate(xlsxFiles):
        if index == 0:
            masterdf = pd.read_excel(path + '/' + xlsFile,index=False)
            
        else:
           
            df = pd.read_excel(path + '/' + xlsFile)

#            masterdf=masterdf.append(df,index=False)
            masterdf = masterdf.append(df, ignore_index=True)

            
    return masterdf

def clearJunk():
    destPath = os.path.join(str(os.getcwd()), 'downloads')
    files = [i for i in os.listdir(destPath) if i not in ('master.csv')]
    subprocess.call(['rm', '-r'] + files)

df = pandasConcat(dlPath)
filePath = dlPath + '/master.csv'
df.to_csv(filePath)
clearJunk()
