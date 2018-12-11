# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 15:19:21 2018

@author: sean
"""

## pandasConcat function finds all xlsx files in the local directory and combines them using pandas into a new csv file

import os
import yaml
import xlrd
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

## Clear junk will get rid of files inside the downloads folder that are not names 'safeFile'

def clearJunk(safeFile):
    destPath = os.path.join(str(os.getcwd()), 'downloads')
    files = [i for i in os.listdir(destPath) if i not in (safeFile)]
    paths = ['downloads/' + x for x in files]
    subprocess.call(['rm', '-r'] + paths)


## If script is run it creates the master csv and clears the old xlsx files

if __name__=="__main__":
   # clearJunk('*.xlsx')
    df = pandasConcat(dlPath)
    filePath = dlPath + '/master.csv'
    df.to_csv(filePath)
    clearJunk('master.csv')
