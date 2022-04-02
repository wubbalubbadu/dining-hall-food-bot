import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

load_dotenv('../../../environment_variables.env')
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
API_KEY = os.getenv('OWM_API_KEY')

with open('info.json') as file:
    data = json.load(file)

browser = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://dineoncampus.com/northwestern/whats-on-the-menu'
browser.get(url)
time.sleep(5)
text = ''
for key in data.keys():
    text += key+':\n'

    browser.find_element(by=By.ID, value="dropdown-grouped__BV_toggle_").click()
    time.sleep(5)
    for option in browser.find_elements(by=By.CLASS_NAME, value='dropdown-item'):
        if option.text == data[key]['loc']:
            option.click() # select() in earlier versions of webdriver
            break

    time.sleep(5) 
    browser.find_element(by=By.XPATH, value=data[key]['time_xpath']).click()
    time.sleep(5) 

    # Give source code to BeautifulSoup
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    time.sleep(15)
    tables = soup.find_all("table", {"class": "table b-table menu-items b-table-caption-top b-table-stacked-md"})

    for i in data[key]['menu_id']:
        table = tables[i]
        dishes = table.find_all('strong')
        for dish in dishes:
                text += dish.string + '\n'
    text += '\n'

browser.close()

client = Client(account_sid, auth_token)
message = client.messages.create(
    body=text,
    from_='+19564773486',
    to='+12247023783'
)
print(message.status)
