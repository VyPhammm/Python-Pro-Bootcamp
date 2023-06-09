from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path= r"D:/Development/chromedriver.exe"
web= "http://orteil.dashnet.org/experiments/cookie/"

service = Service(executable_path=chrome_driver_path) 
driver = webdriver.Chrome(service=service) 
driver.get(web)

#get cookie to click on
cookie= driver.find_element(By.CSS_SELECTOR, '#cookie')

#get store 
items= driver.find_elements(By.CSS_SELECTOR, '#store div')
item_ids= [item.get_attribute("id") for item in items]

cookie_count=driver.find_element(By.CSS_SELECTOR, '#money')
cookie_second= driver.find_element(By.CSS_SELECTOR, '#cps')


timecheck= time.time() + 5
five_min = time.time() + 60*5

while True:
    cookie.click()
    if time.time() > timecheck :

        #get price of upgrade
        all_prices= driver.find_elements(By.CSS_SELECTOR, '#store b')
        item_prices = []

        for price in all_prices:
            price_text= price.text
            if price.text != "":
                cost= int(price_text.split('-')[1].strip().replace(",",""))
                item_prices.append(cost)

        #Create dictionary of store items and prices
        cookie_upgrades= {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]
        
        #Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        #Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        print(affordable_upgrades)

        #Purchase the most expensive affordable upgrade
        try:
            highest_price_affordable_upgrade = max(affordable_upgrades)
            print(highest_price_affordable_upgrade)
            to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

            driver.find_element(By.ID, to_purchase_id).click()
        except:
        #Add another 5 seconds until the next check
            timeout = time.time() + 5
    
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break


    


