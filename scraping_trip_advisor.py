'''
Please Note: We began scraping Trip Advisor but then decided that since we already had enough reviews 
from Skytrax and Seatguru, there was no need. Therefore, this code is only here for information 
purposes - in case someone would like to scrape Trip Advisor, this could be a good place to start :)
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from selenium import webdriver
import os


def scrape():
    homepage_url = "https://www.tripadvisor.com/Airlines"
    homepage=requests.get(homepage_url)
    soup = BeautifulSoup(homepage.content, 'html.parser')
    main_content = soup.find_all(class_ = "mainColumnContent")[0]
    print(len(main_content.find_all(class_ = "airlineData")))
    num_index_pages = 63
    print(main_content.find_next(class_ = "nav next ui_button primary").prettify())
    chromedriver = r"C:\Users\olive\AppData\Local\Programs\ChromeDriver\bin\chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    url = 'http://www.zoover.nl/cyprus'
    driver.get(url)
    driver.find_element_by_class_name('next').click()


if __name__ == '__main__':
    scrape()