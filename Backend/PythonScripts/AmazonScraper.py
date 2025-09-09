from bs4 import BeautifulSoup

from selenium import webdriver
from slenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
import time 
import requests


class ProductInfoScrapper:

    def __init__(self,product_url):
        self.__product_url = product_url 
        self.__product_title = ""
        self.__product_description = ""
        self.__product_price = 0
        self.__product_rating = 0
        self.__product_reviews = []   
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


    def scrapProductPage(self):
        
        print(f"Fetching data from : {self.__product_url}")

        try : 
            # Step - 1 : Fetch 
            response = requests.get(self.__product_url,headers = self.headers)
            response.raise_for_status() # Check the status code 
            # if it is 2__ does nothing , the program continues
            # else if it is 4__ or 5__ , it raises HTTPError exception

            # Step - 2  : Parse
            soup = BeautifulSoup(response.content,'html.parser')

            # Step - 3 : Extract the needed info 

            self._parse_title(soup)
            # self._parse_description(soup)
            # self._parse_price(soup)
            # self._parse_rating(soup)
            # self._parse_reviews(soup)

            print("Scraping Completed!")

        except requests.exceptions.RequestException as e : 
            print(f"Error fetching the URL : {e}")
            return False


    
if __name__ == "__main__" : 
    pc = ProductInfoScrapper("https://www.amazon.in/TIED-RIBBONS-Decorative-Sculpture-Decoration/dp/B0CJYC1VQK/ref=s9_acsd_al_ot_cv2_1_t?_encoding=UTF8&pf_rd_m=A21TJRUUN4KGV&pf_rd_s=merchandised-search-7&pf_rd_r=9AYMW941K6KKFWPP72E2&pf_rd_p=f8c52cdc-e359-4858-af77-1893be7a0da2&pf_rd_t=&pf_rd_i=1380374031")
    pc.scrapProductPage()
