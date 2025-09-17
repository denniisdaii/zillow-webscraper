from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import textwrap
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os 
load_dotenv()
google_form_link = os.getenv("GOOGLE_FORM")
zillow_clone = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(zillow_clone)
soup = BeautifulSoup(response.text, "html.parser")
prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
links = soup.find_all("a", class_="StyledPropertyCardDataArea-anchor")
addresses = soup.find_all('address')
final_address = [textwrap.dedent(address.text.strip().replace("|", "").replace('#','')) for address in addresses]
final_links = [link["href"] for link in links]
final_prices = [price.text.split()[0].replace('/mo', '').replace('+','')for price in prices]
final_data = [final_address, final_prices, final_links]

num_iter = len(final_prices)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
for iter in range(num_iter):
    driver.get(google_form_link)
    time.sleep(3)
    inputs = driver.find_elements(By.CSS_SELECTOR, 'div input[autocomplete="off"]')
    submit_btn = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Submit']")
    for ele in range(len(inputs)):
        inputs[ele].send_keys(final_data[ele][iter])

    time.sleep(2)
    submit_btn.click()
    