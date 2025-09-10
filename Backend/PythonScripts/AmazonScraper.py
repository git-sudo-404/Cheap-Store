from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
import pandas as pd
import time 
import requests
import json


class ProductInfoScrapper:

    def __init__(self,product_url):
        self.__product_url = product_url 
        self.__product_title = ""
        self.__product_description = {}
        self.__product_price = 0
        self.__product_rating = 0
        self.__product_reviews = []  
        self.__no_of_ratings = 0 
        self.__no_of_reviews = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


    def _parse_title(self,soup):
        title_element = soup.find('span',{'id':'productTitle'})
        if(title_element):
            self.__product_title = title_element.text.strip()
            print(f"Product title : {self.__product_title}")
        else :
            print("Couldn't find product title")
    
    def _parse_description(self,soup):
        desc_table = soup.find("table",{"id":"productDetails_techSpec_section_1"})
        if desc_table : 
            for row in desc_table.find_all('tr'):
                key_element = row.find('th')
                value_element = row.find('td')
                if(key_element and value_element):
                    key = key_element.text.strip()
                    val = value_element.text.strip().replace('\u200e','')
                    self.__product_description[key] = val

            print("Product Description")
            print(json.dumps(self.__product_description,indent = 2))

        else :
            print("Couldn't find product info")



    def _parse_price(self,soup):
        price_element = soup.find("span",{"class":"a-price-whole"})
        if(price_element):
            self.__product_price = price_element.text.strip()
            print(f"Price : {self.__product_price}")
        else:
            print("Price not found")


    def _parse_rating(self,soup):
        rating_element = soup.find('span',class_='a-icon-alt') 
        if rating_element:
            rating_text = rating_element.get_text(strip = True)
            rating_value_str = rating_text.split(' ')[0] # -> "3.8"
            rating_value_float = float(rating_value_str) # -> 3.8
            self.__product_rating = rating_value_float
            print(f"Product Rating : {self.__product_rating}")
        else:
            print("Couldn't find product rating")

    def _parse_no_of_ratings(self,soup):
        no_of_ratings_element = soup.find('span',{'id':'acrCustomerReviewText'})
        if no_of_ratings_element:
            no_of_ratings_text = no_of_ratings_element.text.strip()
            no_of_ratings_val_str = no_of_ratings_text.split(' ')[0]
            no_of_ratings_val = float(no_of_ratings_val_str)
            self.__no_of_ratings = no_of_ratings_val
            print(f"No of Rating : {self.__no_of_ratings}")
        else:
            print("Couldn't find no of ratings")


    def scrapProductPage(self):
        
        print(f"Fetching data from : {self.__product_url}")

        try : 
            # Step 1: Set up and launch a Chrome browser using Selenium
            options = webdriver.ChromeOptions()
            options.add_argument('--headers') # Run in background without opening a UI 
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # This automatically downloads and manages the correct driver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Step 2: Fetch the page 
            driver.get(self.__product_url)
            time.sleep(2)   # Wait for Js to load 

            #Step 3: Get the fully rendered page source 
            page_source = driver.page_source 
            driver.quit() # Close the browser 

            #Step 4: Parse with BeautifulSoup 
            soup = BeautifulSoup(page_source,'html.parser')

            self._parse_title(soup)
            self._parse_description(soup)
            self._parse_price(soup)
            self._parse_rating(soup)
            self._parse_no_of_ratings(soup)
            # self._parse_no_reviews(soup)
            # self._parse_reviews(soup)


        except requests.exceptions.RequestException as e : 
            print(f"Error fetching the URL : {e}")
            return False


    
if __name__ == "__main__" : 
    pc = ProductInfoScrapper("https://www.amazon.in/TIED-RIBBONS-Decorative-Sculpture-Decoration/dp/B0CJYC1VQK/ref=s9_acsd_al_ot_cv2_1_t?_encoding=UTF8&pf_rd_m=A21TJRUUN4KGV&pf_rd_s=merchandised-search-7&pf_rd_r=9AYMW941K6KKFWPP72E2&pf_rd_p=f8c52cdc-e359-4858-af77-1893be7a0da2&pf_rd_t=&pf_rd_i=1380374031")
    pc.scrapProductPage()
