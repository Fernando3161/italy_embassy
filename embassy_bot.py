# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
import time
import logging
logging.basicConfig(
    filename='Attempts.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def send_message(chat_id=5874954138, message="No meetings found"):
    with open('data.json') as json_file:
        data = json.load(json_file)
    TOKEN = data["telegram"]["token"]
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()

# %%


def check_dates(i=None):
    with open('data.json') as json_file:
        data = json.load(json_file)
    USER = data["info_it"]["user"]
    PASS = data["info_it"]["pass"]
    CHAT_FP = data["telegram"]["chat_fp"]
    CHAT_KF = data["telegram"]["chat_kf"]

    driver = webdriver.Chrome()
    driver.get("https://prenotami.esteri.it/")
    assert "Home Page - Prenot@Mi" in driver.title

    username = driver.find_element(By.ID, "login-email")
    username.clear()
    username.send_keys(USER)

    password = driver.find_element(By.ID, "login-password")
    password.clear()
    password.send_keys(PASS)

    driver.find_element(By.CLASS_NAME, "button").click()
    driver.find_element(By.LINK_TEXT, "Prenota").click()
    time.sleep(5)

    try:
        driver.find_element(
            By.XPATH, "/html/body/main/div[3]/div/table/tbody/tr[3]/td[4]/a/button").click()
        try:
            a = driver.find_element(By.CLASS_NAME, "jconfirm-content")
            if a.text == 'Al momento non ci sono date disponibili per il servizio richiesto':
                send_message(chat_id=CHAT_FP, message="No meetings available")
                logging.info("0: No meetings available")
                #send_message(chat_id=CHAT_KF, message="No meetings available")
                print("No dates available")

            else:
                send_message(
                    chat_id=CHAT_FP, message="Possible dates available. Check https://prenotami.esteri.it/")
                send_message(
                    chat_id=CHAT_KF, message="Possible dates available. Check https://prenotami.esteri.it/")
                logging.info("1: WARNING: Meetings available")
                print("Possible dates available")

        except:
            send_message(
                chat_id=CHAT_FP, message="Possible dates available. Check https://prenotami.esteri.it/")
            send_message(
                chat_id=CHAT_KF, message="Possible dates available. Check https://prenotami.esteri.it/")
            logging.info("2: No error message found. Maybe meetings available")
            print("Possible dates available")

    except:
        send_message(chat_id=CHAT_FP,
                     message="Element not found. Skipping to next iteration")
        logging.info("3: Element not found. Skipping to next iteration")

        print("Element not found. Skipping to next iteration")

    if i == 1000:
        send_message(chat_id=CHAT_FP,
                     message="Last iteration. RESTART application")


# %%
def main():
    i = 0
    while i < 1000:
        check_dates(i)
        time.sleep(600)
        i += 1


if __name__ == "__main__":
    main()
