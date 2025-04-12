from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import logging

logging.basicConfig(
    filename=r'C:\Users\Bogdan\Desktop\Proveri mejl\Proveri mejl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

url = "https://aurora.ekof.bg.ac.rs/mail/src/login.php"
username_dugme = "//tr[2]/td/table/tbody/tr[1]/td[2]/input"
password_dugme = "//tr[2]/td/table/tbody/tr[2]/td[2]/input[1]"
potvrdi_login = "//tr[3]/td/center/input"
novi_mejl1_dugme = "//tr/td/table/tbody/tr[2]/td[5]//a"
user_key = "u6vfm6ffbx9c2isn3ffzgcbi321j3y"  
app_token = "am387kwhzhtu3cc1z1v4dfcaha3ub5"
usernames = ['s211457', 's210172']
sifre = ['sifra1', 'sifra2']

def login(username, password):
    driver.find_element(By.XPATH, username_dugme).send_keys(username)
    driver.find_element(By.XPATH, password_dugme).send_keys(password)
    driver.find_element(By.XPATH, potvrdi_login).click()
def pronadji_poslednji_mejl():
    driver.implicitly_wait(10)
    driver.switch_to.default_content()
    driver.switch_to.frame('right')
    novi_mejl = driver.find_element(By.XPATH, novi_mejl1_dugme)
    tekst = novi_mejl.text
    font_weight = novi_mejl.value_of_css_property('font-weight')
    isbold = int(font_weight) >= 700
    return isbold, tekst

def posalji_notifikaciju(user_key, app_token, message):
    payload = {
        "token": app_token,
        "user": user_key,
        "message": message
    }
    response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
    if response.status_code == 200:
        logging.info("Obavestenje je poslato.")
    else:
        logging.error(f"Obavestenje nije poslato: {response.status_code}")

logging.info("Pocetak")
driver = webdriver.Chrome()
driver.get(url)

for user, password in zip(usernames, sifre):
    try:
        logging.info(f"Prijavljivanje kao {user}.")
        login(user, password)

        isbold, tekst = pronadji_poslednji_mejl()
        if isbold:
            logging.info(f"Pronadjen mejl za {user}")
            posalji_notifikaciju(user_key, app_token, f"Stigao je mejl za {user}:{tekst}")
        else:
            logging.info(f"Nema novih mejlova za {user}.")

        driver.get(url)
    except Exception as e:
        logging.error(f"Doslo je do greske za {user}: {str(e)}")
    
    finally:
        logging.info(f"Zavrseno procesiranje korisnika {user}.")

driver.quit()
logging.info("Kraj")