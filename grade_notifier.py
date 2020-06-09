from selenium import webdriver
from time import sleep
import json

path = "c:\\users\\aboud\\web drivers\\chromedriver.exe"


def click_button(driver):
    button = driver.find_element_by_id('idSIButton9')
    sleep(0.4)
    button.click()
    sleep(0.4)


def get_credentials():
    with open('imc_credentials.json') as f:
        cred = json.load(f)
    return cred


def get_last_grade():
    cred = get_credentials()
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(path, options=op)
    driver.get('https://imc.today/')
    sleep(0.75)
    login = driver.find_element_by_name('loginfmt')
    login.send_keys(cred['account'])
    click_button(driver)
    sleep(0.75)
    password = driver.find_element_by_name('passwd')
    password.send_keys(cred['password'])
    click_button(driver)
    sleep(0.75)
    button = driver.find_element_by_xpath("//input[@value='Yes']")
    button.click()
    sleep(1.5)
    driver.switch_to.window(driver.window_handles[-1])
    get_last = driver.find_element_by_xpath('//*[@data-categoryid="4"]/descendant::h4').get_attribute('innerHTML')
    with open('subjects.txt', 'r') as f:
        file = f.read()
    with open('subjects.txt', 'a') as f:
        if get_last in file:
            print(f'No new subjects. last subject is {get_last}')
            return None
        else:
            f.write(get_last + '\n')
            return 'New grade!\n' + get_last
