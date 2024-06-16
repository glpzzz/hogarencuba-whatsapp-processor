import random
import re
import time

from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from common.hogarencuba import HogarEnCubaClient


def process():
    print("this is dequeue")

    hec_client = HogarEnCubaClient()
    item = hec_client.get_first_unsent()

    if item is None:
        return

    print(item["phone"] + " " + item["metadata"])

    hec_client.mark_message_as_tried(item["id"])

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=./data")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

    try:

        phone = item["phone"]

        # sanitize the phone number
        phone = re.sub(r"\D", "", phone)
        message = quote(item["message"])

        driver.get(f"https://web.whatsapp.com/send/?phone={phone}&text={message}&type=phone_number")
        time.sleep(60 + random.randint(0, 30))

        message_field = driver.find_element(
            By.XPATH,
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p',
        )
        message_field.send_keys(Keys.ENTER)

        hec_client.mark_message_as_sent(item["id"])

    except NoSuchElementException:
        print(f"Can't open the chat with {item["phone"]}")
        hec_client.set_message_output(item["id"], "Not a WhatsApp number")
    except Exception as e:
        print(f"It crashed because: {str(e)}")
        hec_client.set_message_output(item["id"], str(e))
    finally:
        time.sleep(5 + random.randint(0, 5))
        driver.quit()
