from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys
import os
import uuid
import requests
import urllib

import unittest, time, re

#what do you want to search for?
SEARCH_QUERY = "" #"dog"

#specify the path where the images will be downloaded to. 
BASEPATH = "" #"/home/bernhard/pexels/"

#how often do you want to scroll down?
NUMBER_OF_SCROLL_DOWNS = 20


DELAY_BETWEEN_EVERY_SCROLL_DOWN = 1

DOWNLOADPATH = BASEPATH + os.path.sep + SEARCH_QUERY


def download(url):
    urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
    p = DOWNLOADPATH + os.path.sep + str(uuid.uuid4())
    urllib.urlretrieve(url, p)


if __name__ == "__main__":
    if BASEPATH == "":
        print("Please set the BASEPATH first!")
        sys.exit(1)

    if not os.path.exists(BASEPATH):
        print("%s is not a valid path!" %(BASEPATH,))
        sys.exit(1)

    #create directory if not exists
    if not os.path.exists(DOWNLOADPATH):
        os.makedirs(DOWNLOADPATH)
        #check again (paranoia check ;))
        if not os.path.exists(DOWNLOADPATH):
            print("%s doesn't exist!" %(DOWNLOADPATH,))


    if len(os.listdir(DOWNLOADPATH)) != 0:
        print("Folder %s needs to be empty!" %(DOWNLOADPATH,))
        sys.exit(1)

    if SEARCH_QUERY == "":
        print("SEARCH_QUERY needs to be set!")
        sys.exit(1)


    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    base_url = "https://www.pexels.com"
    verificationErrors = []
    accept_next_alert = True

    driver.get(base_url + "/search/" + SEARCH_QUERY + "/")
    for i in range(1, NUMBER_OF_SCROLL_DOWNS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(DELAY_BETWEEN_EVERY_SCROLL_DOWN)

    elems = driver.find_elements_by_xpath("//img[@srcset]")
    ctr = 0
    for elem in elems:
        ctr += 1
        imgs = elem.get_attribute("srcset")
        imgUrl = imgs.split(', ')[0]
        imgBaseUrl = imgUrl.split('?')[0]
        try:
            downloadUrl = imgBaseUrl + "?w=1000&auto_compress&cs=tinysrgb 1x"
            print("downloading #%d, %s" %(ctr, downloadUrl,))
            download(downloadUrl)
        except:
            pass

    print("DONE")
