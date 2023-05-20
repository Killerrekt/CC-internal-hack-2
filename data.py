from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import mysql.connector
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
import os

def open_vtop(driver):
    while(True):
        button = driver.find_element(By.XPATH,'//*[@id="stdForm"]/a/div/div[2]/button')
        button.click()
        time.sleep(3)
        try:
            driver.find_element(By.XPATH,'//*[@id="captchaStr"]')
        except Exception:
            button  = driver.find_element(By.XPATH,'//*[@id="loginBox"]/div/div[3]/div/a/strong/i')
            button.click()
            time.sleep(3)
        else:
            load_dotenv()
            pss = os.environ['PASSWORD']
            user = os.environ['USER']
            username = driver.find_element(By.XPATH,'//*[@id="username"]')
            username.send_keys(user)
            password = driver.find_element(By.XPATH,'//*[@id="password"]')
            password.send_keys(pss)
            time.sleep(1)
            button = driver.find_element(By.XPATH,'//*[@id="submitBtn"]')
            button.click()
            break
    time.sleep(15)

def clubs(driver):
    open_vtop(driver)
    button = driver.find_element(By.XPATH,'//*[@id="vtopHeader"]/div/button[1]/span')
    button.click()
    time.sleep(0.5)
    button = driver.find_element(By.XPATH,'//*[@id="acMenuItemHDG0101"]/button/span')
    button.click()
    time.sleep(0.5)
    button = driver.find_element(By.XPATH,'//*[@id="acMenuCollapseHDG0101"]/div/a[4]')
    button.click()
    time.sleep(3)
    driver.find_element(By.TAG_NAME,'body').click()
    
    con = mysql.connector.connect(host="localhost",password="140604",user="root",charset="utf8")
    cur = con.cursor()
    cur.execute("create database if not exists clubs")
    cur.execute("use clubs")
    cur.execute("create table if not exists event(club varchar(255), event varchar(255), days varchar(255), timing varchar(255), no_of_days varchar(255), Venue varchar(255))")
    
    select = Select(driver.find_element(By.XPATH,'//*[@id="dataTable1_length"]/label/select'))
    select.select_by_visible_text('100')

    driver.find_element(By.XPATH,'//*[@id="dataTable1"]/thead/tr/th[1]').click()
    
    source = driver.page_source
    soup = BeautifulSoup(source,'html.parser')
    k = soup.find('td').text
    
    driver.find_element(By.XPATH,'//*[@id="dataTable1"]/thead/tr/th[1]').click()

    tablecontents = soup.find_all('td')
    j = 1
    l = []
    for i in tablecontents[:int(k)*10]:
        if(j%10 not in (1,4,0,8)):
            l.append(i.text)
        if(j%10 == 0):
            ins = ("insert ignore into event values (%s ,%s ,%s ,%s ,%s ,%s)")
            cur.execute(ins,l)
            l = []
        j+=1
        print()
    con.commit()
    con.close()
    driver.close()

def calendar(driver):
    button = driver.find_element(By.XPATH,'//*[@id="vtopHeader"]/div/button[1]/span')
    button.click()
    time.sleep(0.5)
    button = driver.find_element(By.XPATH,'//*[@id="acMenuItemHDG0067"]/button/span')
    button.click()
    time.sleep(0.5)
    calender = driver.find_element(By.XPATH,'//*[@id="acMenuCollapseHDG0067"]/div/a[19]')
    calender.click()
    time.sleep(3)
    driver.find_element(By.TAG_NAME,'body').click()
    print("It is done?")

options = webdriver.ChromeOptions()
s = Service('D:\python\chromedriver.exe')
options.add_extension('Viboot.crx')
driver = webdriver.Chrome(service=s,options=options)
driver.get('https://vtop.vit.ac.in/vtop/login')
time.sleep(5)

clubs(driver)