# Creating Simple Whatsapp "API" or "Bot"
# using selenium webdriver (chromedriver)
# 
# Author    : Muhammad Rafiul Ilmi Syarifudin
# Created   : June 27, 2019
# 
# prerequisite :
# - Selenium Python module 
# - Chromedriver (https://chromedriver.storage.googleapis.com/index.html?path=2.36/)

# Import selenium 
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By

# Define path to chromedriver
driver = webdriver.Chrome('E:\\chromedriver.exe')

# Navigate driver to go to https://web.whatsapp.com/
driver.get("https://web.whatsapp.com")
wait = WebDriverWait(driver, 600)       # Set time out 600 ms

# Set target to test send Whatsapp message via python script
# like your friend's name or group name
# put your target look like this -> '"Friend's name"'
# beware single quote and double quote
to = '"BIA Product Development"' 

# prepare your message to send
msg = "Hey, I'm sending this message using python script powered by selenium"

# Now, it's time to select elements at web.whatsapp.com 
# such as your friends or group chat and input text form using XPATH
# XPATH of target
e_target = '//span[contains(@title,' + to + ')]'
target = wait.until(EC.presence_of_element_located((By.XPATH, e_target)))
target.click()
# XPATH of input text form
e_input = '//div[@contenteditable="true"][@dir="ltr"][@data-tab="1"]'
input_box = wait.until(EC.presence_of_element_located((By.XPATH, e_input)))

# Yeay! Send message to target
input_box.send_keys(msg + Keys.ENTER) 