from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import getpass
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import time
driver = webdriver.Chrome("/Users/vamilgandhi/Documents/chromedriver") # add your chrome driver here

executor_url = driver.command_executor._url
session_id = driver.session_id
job = []



def cmu_login(uname, upass):
    driver.get("https://cmu.joinhandshake.com/")
    driver.find_element_by_css_selector(".sso-button").click()
    print('Logging into your handshake account...')
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("passwordinput")
    username.send_keys(uname)
    password.send_keys(upass)
    driver.find_element_by_name("_eventId_proceed").click() #submit button
    

    #Duo Authentication
    time.sleep(5)
    driver.switch_to_frame("duo_iframe")
    driver.find_element_by_xpath('//*[@id="auth_methods"]/fieldset/div[1]/button').click()
    time.sleep(10)
    driver.switch_to_default_content()

    print('Logged in successfully')

def get_profile(jlink):
    try:
        jtittle = driver.find_element_by_xpath('//*[@id="skip-to-content"]/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/a').text
        jcompany = driver.find_element_by_xpath('//*[@id="skip-to-content"]/div[2]/div/div[1]/div/div/div/div/div[1]/div[3]/div/div[2]/div[1]').text
        jdeadline = driver.find_element_by_xpath('//*[@id="skip-to-content"]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]').text
        jworkauth = driver.find_element_by_xpath('//*[@id="skip-to-content"]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[3]/div[2]').text
        new = ((jtittle,jcompany,jdeadline,jworkauth, jlink))
        job.append(new)
        print(job)
    except:
        print("Couldn't scrap job")

def scrap_jobs():
    f = open('./links.txt', 'r')
    for x in f:
        print(x)
        if x == '':
            break
        driver.get(x)
        time.sleep(5)
        get_profile(x)
    
    df = pd.DataFrame(job,columns=['Job Tittle','Company', 'Deadline', 'US Work Authorization Status','Link'])
    df.to_csv('jobs.csv', mode = 'a') # add Header =  False to append to existing file
    

if __name__ == "__main__": 
    # add your cmu username and password here
    username = '' 
    password = ''


    cmu_login(username,password)
    time.sleep(10)
    scrap_jobs()