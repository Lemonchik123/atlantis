import traceback

from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.keys import Keys
import os
from twocaptcha import TwoCaptcha
import string
from user_agent import *



proxy_login = "логин от прокси"
proxy_password = "пароль от прокси"

proxy_options = {
    "proxy": {
        "https": f"https://{proxy_login}:{proxy_password}@айпи:порт от прокси"
    }
}

def xpath_exists(xpath, driver):
    try:
        driver.find_element(By.XPATH, xpath)
        exist = True
    except NoSuchElementException:
        exist = False
    return exist


def clickble(selector, driver, timeout=5):
    try:
        if WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, selector))):
            return True
        else:
            return False
    except:
        pass


def doit(login, password, verifmail, driver):
    try:
        driver.maximize_window()
        driver.get("https://trade.atlantiscex.com/r/B004101368772")
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        time.sleep(1)
        letters_and_digits = string.ascii_letters + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 16))
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(rand_string)
        time.sleep(1)
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(login)
        time.sleep(1)
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Lemonchik12345!")
        time.sleep(1)
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, "//input[@id='password-confirm']")))
        driver.find_element(By.XPATH, "//input[@id='password-confirm']").send_keys("Lemonchik12345!")
        time.sleep(1)
        # scroll
        html = driver.find_element(By.TAG_NAME, 'html')
        for i in range(15):
            html.send_keys(Keys.DOWN)
            time.sleep(0.2)

        # captha
        captcha = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div/form/div[7]/span/img")
        captcha.screenshot("captcha.png")
        api_key = "61bfe39f2c9675fc0bf8742ff92bf1cd"
        solver = TwoCaptcha(api_key)

        config = {
            'server': '2captcha.com',
            'apiKey': '61bfe39f2c9675fc0bf8742ff92bf1cd',
            'softId': 123,
            'callback': 'https://your.site/result-receiver',
            'defaultTimeout': 120,
            'recaptchaTimeout': 600,
            'pollingInterval': 10,
        }

        result = solver.normal('captcha.png')
        result = result['code']
        driver.find_element(By.ID, "captcha").send_keys(result)
        time.sleep(1)

        # I gree Terms of use
        driver.find_element(By.XPATH, "//input[@name='check']").click()
        time.sleep(1)

        # sign up button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)

        # verif mail
        driver.get("https://account.mail.ru/login")

        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        driver.find_element(By.XPATH, "//input[@name='username']").send_keys(login)  # EMail
        time.sleep(1)
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
        driver.find_element(By.XPATH, "//button[@type='submit']").click()  # Log
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)  # Password
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        driver.find_element(By.XPATH, "//button[@type='submit']").click()  # Log
        print("Авторизация успешная!")
        time.sleep(9)

        # verifmail
        # if WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))):
        if clickble("//input[@type='text']", driver):
            driver.find_element(By.XPATH, "//input[@type='text']").send_keys(verifmail)
            time.sleep(2)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
        else:
            pass

        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@type='button']"))).click()
        #
        # driver.find_element(By.XPATH, "//input[@class='mail-operands_dynamic-input__input--HbfQR mail-operands_dynamic-input__inputCompact--F5HoI _3pRLYQt59tmiwn0Ugfy9W5']").send_keys("info@atlantiscex.com")
        # time.sleep(1)
        # driver.find_element(By.XPATH, "//span[@class='_1Sq-e9MVzbKWUgdGRPfVlE ozp_6goCk56QeWXu5EPqS']").click()
        # time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Atlantis')]"))).click()
        time.sleep(2)

        href = driver.find_element(By.XPATH, "//a[contains(text(), 'Verify to proceed')]").get_attribute('href')
        print("верифнули емеил")
        driver.get(f'{href}')

        # логинимся в аккаунт
        time.sleep(6)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='email']"))).send_keys(login)
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys("Lemonchik12345!")
        time.sleep(1)

        # scroll
        html = driver.find_element(By.TAG_NAME, 'html')
        for i in range(5):
            html.send_keys(Keys.DOWN)
            time.sleep(0.1)

        # captcha
        captcha = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div/form/div[3]/span/img")
        captcha.screenshot("captcha.png")

        api_key = "ваш апи кей капчи"
        solver = TwoCaptcha(api_key)

        config = {
            'server': '2captcha.com',
            'apiKey': '61bfe39f2c9675fc0bf8742ff92bf1cd',
            'softId': 123,
            'callback': 'https://your.site/result-receiver',
            'defaultTimeout': 120,
            'recaptchaTimeout': 600,
            'pollingInterval': 10,
        }

        result = solver.normal('captcha.png')
        result = result['code']
        driver.find_element(By.ID, "captcha").send_keys(result)
        time.sleep(1)

        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(9)
    except Exception as ex:
        traceback.print_exc()

    finally:
        driver.close()
        driver.quit()


def main(login, password, verifmail):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={random.choice(user_agents_list)}")

        s = Service(executable_path=r"ваш хром драйвер")
        driver = webdriver.Chrome(
            service=s,
            options=options,
            seleniumwire_options=proxy_options)
        doit(login, password, verifmail, driver)

    except Exception as ex:
        traceback.print_exc()



def maker():
    acc = 0
    while True:
        try:
            file = open("dannue.txt", 'r')
            data = file.read()
            file.close()
            data = data.split("\n")
            danni = data[acc]
            danni = danni.split(":")
            login = danni[0]
            password = danni[1]
            verifmail = danni[2]
            print(login, password, verifmail)
            print(f"Получен логин и пароль от {acc + 1} акка")
            time.sleep(1)
            acc += 1
            main(login, password, verifmail)
        except Exception as ex:
            traceback.print_exc()


if __name__ == '__main__':
    maker()
