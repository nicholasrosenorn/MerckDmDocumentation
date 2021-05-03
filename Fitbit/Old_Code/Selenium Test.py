#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 11:01:24 2020

@author: joshuak
"""

#from selenium import webdriver
#browser = webdriver.Firefox()

import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import json


from selenium import webdriver
from selenium.webdriver import Firefox

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.add_argument("-headless")
browser = Firefox(executable_path = '/Users/joshuak/Documents/STAT190/Corporate Partners/Fitbit/geckodriver', options=fireFoxOptions)

browser.get('https://google.com')

browser.close()

import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import json

#Both the Client ID and Client Secret come from when Fitbit site after registering an app
CLIENT_ID = '22BH28' #Mine:'22BKP3'
CLIENT_SECRET = '78a4838804c1ff0983591e69196b1c46' #Mine:'1a42e97b6b4cc640572ae5cf10a7d0b0'

#Authorization Process
# opens website
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
# opens website (? but not really?)
server.browser_authorize()


'''
def connectFirefox():
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options  = options)
    print("Firefox Headless Browser Invoked")
    return driver

def main():
    #driver = connectChrome()
    driver = connectFirefox()
    driver.get("https://www.archlinux.org/")
    print("Headless Browser closing")
    driver.quit()
   
main()
'''