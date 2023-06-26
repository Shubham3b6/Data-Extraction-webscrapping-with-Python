import time
import json
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


def to_json(data_list):
    hash_obj = json.dumps(data_list,indent=4)
    with open("Meesho Extracted Product.json", "w") as ts:
        ts.write(hash_obj)

def to_csvfile():
    with open('Meesho Extracted Product.json') as json_file:
        data = json.load(json_file)

    # Create a new CSV file and write the data
    with open('Meesho_Extracted_Product_task-1.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    



def get_soup(url):
    from bs4 import BeautifulSoup as bs
    import requests
    headers={'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
    #     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    with requests.get(url, headers = headers, stream = True) as res:
        soup = bs(res.text, 'html.parser')
    return soup

def get_data(slug="slugName"):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    data_list = []
    url = "https://www.meesho.com/search?q=Loreal&searchType=manual&searchIdentifier=text_search"
    options = webdriver.ChromeOptions()
    #options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    options = webdriver.ChromeOptions()
    driver.get(url)
    time.sleep(3)

    
    list_name=driver.find_elements(By.XPATH,"//*[@id='__next']/div[3]/div/div[3]/div[2]/div[2]/div/div/a")
    list_name=[i.get_attribute('href') for i in list_name]   
    # print(list_name)
    
    


    for i in list_name:
        driver.get(i)
        time.sleep(3)
        df={}
        Product_URLs,Price,Title,Image_URL,Seller_Name,Store_URL='','','','','',''
        
        Product_URLs=(i)
        # print(Product_URLs)

        try:
            Title=driver.find_element(By.XPATH,"//*[@id='__next']/div[3]/div/div[2]/div[1]/span").text
            # print(Title)
        except:
            pass
        try:
            Price=driver.find_element(By.XPATH,"//*[@id='__next']/div[3]/div/div[2]/div[1]/div[1]/h4").text
            # print(Price)
        except:
            pass

        try:
            Image_URL=driver.find_element(By.XPATH,"//*[@id='__next']/div[3]/div/div[1]/div/div[2]/div[1]/picture/img").get_attribute('src')
            # print(Image_URL)
        except:
            pass




        if Product_URLs :
            df['Product_URLs']=Product_URLs

        if Title :
            df['Title']=Title

        if Price:
            df['Price']=Price.replace("\u20b9", "")
    
        if Image_URL:
            df['Image_URL']=Image_URL


    

        data_list.append(df) 

        
    driver.quit()     
    return data_list
    

    

if __name__ =="__main__":
    data_list = get_data('slug_name')
    #print(data_list)
    to_json(data_list)
    to_csvfile()


	