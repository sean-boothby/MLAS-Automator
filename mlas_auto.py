# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 21:47:45 2018
@author: sean
"""
import os
import sys
import time
import yaml
import random
import datetime
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


idNumberMaster = []

config = yaml.safe_load(open("/home/sean/tools/test/MLAS-Automator/config/config.yml"))
#gsbucket = config['gsbucket']['src']

queryNum = sys.argv[1]
queryNum = int(queryNum)
queryNum = queryNum*1000


dlPath = config['downloads']['downloadpath']
path = '/home/sean/tools/test/MLAS-Automator/chromedriver'


options = webdriver.ChromeOptions()
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.default_directory": str(dlPath) , "download.extensions_to_open": "applications/pdf"}
options.add_experimental_option("prefs", profile)
options.add_argument("--headless")
driver = webdriver.Chrome(path, chrome_options=options)
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': dlPath}}
command_result = driver.execute("send_command", params)

starting_url = 'https://www.one-key.gov.on.ca/iaalogin/IAALogin.jsp'


def main(): 
    driver.get(starting_url)
    onekeyLogin()
    driver.maximize_window()
    driver.get('https://www.mlas.mndm.gov.on.ca/mlas/index.html#/searchClient')
    time.sleep(2)
    driver.get('https://www.mlas.mndm.gov.on.ca/mlas/index.html#/searchClient')
    time.sleep(3)
    mlasCheck()
    clientSearch()
    pageFlip()
    time.sleep(2)
    driver.get('https://www.mlas.mndm.gov.on.ca/mlas/index.html#/reportClient')
    time.sleep(2)
    mlasCheck()
    queryRange = idNumberMaster[queryNum-1000:queryNum]
    print('Length of search range is: ' + str(len(queryRange)) + ' for process- ' + str(queryNum/1000))
    for idNum in queryRange:
        ReportQuery(idNum)
        FinalQuery()
        dl = download()
        if dl == 'Not clickable':
            continue
        elif dl == False:
            for n in range(5):
                if dl == False:
                    dl = download()
                else:
                    break
        driver.get('https://www.mlas.mndm.gov.on.ca/mlas/index.html#/reportClient')
    driver.quit()
    
    ## Finished with selenium, lets organize and sync our data then finally clear our download folder
    
#        remote(gsbucket + '/' + filePath)



def onekeyLogin():
    try:
        userName = driver.find_element_by_xpath('//input[@id="ldap_user"]')
        userName.click()
        time.sleep(1)
        userName.send_keys('map.life')
        password = driver.find_element_by_xpath('//input[@id="ldap_password"]')
        password.click()
        time.sleep(1)
        password.send_keys('maplifeTeam#1')
        time.sleep(1)
        signinButton = driver.find_element_by_xpath('//input[@id="Login"]')
        signinButton.click()
        print('You have signed in to ONe-key! Login performed nominally.')
    except Exception as e:
        print('Login has failed - check for changes in xpath')


def mlasCheck():
    if 'mlas.mndm.gov.on.ca' in driver.current_url:
        print('Good job you are in MLAS')
    else:
        print('We are not at MLAS - script needs fixing')

def clientSearch():
    try:
        btnX = '//div[@class="multiselect-parent btn-group dropdown-multiselect"]/button[@class="dropdown-toggle ng-binding btn btn-default"]'
        btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, btnX)))
        btn.click()
        cmpBtnX = '//span[@class="glyphicon glyphicon-ok"]' 
        cmpBtn = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, cmpBtnX)))
        cmpBtn[0].click()
        driver.find_elements_by_xpath('//span[@class="btn-label ng-binding"]')[1].click()
    except:
        print('We failed to click')

def pageFlip():
    while True:
        try:
            clientScrape()
            nextX = '//li[@class="pagination-next ng-scope"]/a[@class="ng-binding"]'
            nextBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, nextX)))
            nextBtn.click()
            time.sleep(1)
        except:
            break
            print('We got all of the company Id numbers!')

def clientScrape():
    try:
        idsX = '//a[@id="popupClientInfoLnkId"]'
        idsNums = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, idsX)))
        for idnum in idsNums:
            idNumberMaster.append(idnum.text)
    except:
        print('Failed to scrape')

def ReportQuery(idNum):
    try:
        repQue = '//input[@id="clientIdInptId"]'
        repQuery = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, repQue)))
        repQuery.click()
        repQuery.send_keys(str(idNum))
        time.sleep(1)
        driver.find_element_by_xpath('//button[@class="btn btn-labeled btn-primary"]/span').click()
        time.sleep(1)
        print('I think we ran our query!!!')
    except:
        print('We did not run our search')

def FinalQuery():
    clientId = '//a[@id="clientIdLnkId0"]'
    IdButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, clientId)))
    IdButton.click()
    time.sleep(10)

def download():
    try:
        clickcheck = dlClick()
        if clickcheck == 'Not clickable':
            return 'Not clickable'
        for i in range(2000):
            try:
                rename()
                break
            except:
                time.sleep(0.1)
                continue
        print('We should have our file downloaded, lets check')
        rename()
    except:
        print('We did not click the download button, better try again')
        time.sleep(20)
        return False
    
def dlClick():
    try:
        dlButtonX = '//button[@class="btn btn-labeled btn-primary"]/span'
        dlButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, dlButtonX)))
        dlButton.click()
    except:
        print('We are jumping ahead')
        driver.get('https://www.mlas.mndm.gov.on.ca/mlas/index.html#/reportClient')
        time.sleep(4)
        return 'Not clickable'

def downloadCheck():
    try:
        dlTime = os.path.getmtime(dlPath + str('/ClientReport'))
        dlTime = datetime.fromtimestamp(dlTime)
        now = datetime.now()
        deltaDays = (now-dlTime).days
        print(deltaDays)
        
        if deltaDays > 0:
            return False
        else:
            return True
    except:
        return False

def rename():
    old_file = os.path.join(str(dlPath), "ClientReport.xlsx")
    new_file = os.path.join(str(dlPath), "ClientReport" + str(int(time.time())) + str(float(random.randint(0,100) + random.randint(1,99))/100) +'.xlsx')
    os.rename(old_file, new_file)
    
main()

