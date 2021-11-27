import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

s=Service('C:\\Users\\Alexb\\Downloads\\tes\\chromedriver.exe')
driver = webdriver.Chrome(service=s)  # Optional argument, if not specified will search path.

driver.get('http://www.google.com/');


time.sleep(5) # Let the user actually see something!

driver.get("")
search_box = driver.find_element('search')

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(5) # Let the user actually see something!

driver.quit()