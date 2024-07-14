"""
THIS SCRIPT IS DESIGNED FOR PERSONAL USE, MODIFY IT ACCORDING TO YOUR OWN NEEDS, NO NEED TO CHANGE WHOLE SCRIPT JUST MAJOR KEYWORDS [BEST IF YOU USE IT FOR AFFILIATE PURPOSES]
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
import logging


chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Set path to chromedriver as per your configuration
webdriver_service = Service('chromedriver/chromedriver.exe')

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


# Configure logging
logging.basicConfig(filename='image_details.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    data = []

    # driver = webdriver.Chrome()
    driver.get(
        "https://thedealapp.in/Deals/category?size=0&deals=true&stores=Amazon")

    deal_containor = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "cc_detailsBox_mini")
        )
    )

    anchor_tag = deal_containor.find_element(
        By.TAG_NAME, "a").get_attribute("href")

    print(f"Unique URL: {anchor_tag}")

    found = False
    with open("a.txt", "r") as f:
        for line in f:
            if anchor_tag in line.strip():
                found = True
                print("Deal page already scraped")
                break

    if not found:
        print("-- NEW DEAL FOUND --")
        with open("a.txt", "a") as g:  # Use 'a' to append instead of 'w+'
            g.write(f"{anchor_tag}\n")

        driver.get(anchor_tag)

        deal_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body[@class='no-touch']/div[@id='app']/main[@class='App-content']/div[@id='content']/div[@class='DiscussionPage']/div[@class='DiscussionPage-discussion']/header[@class='Hero DiscussionHero DiscussionHero--colored']/div[@class='container']/ul[@class='DiscussionHero-items']/li[@class='item-discussionDealDetails1']/div[@class='cc_custDetailsHeader']/div[@class='cc_custDetailsHeaderRightBox']/div[4]/a[@class='Button Button--primary hasIcon']"))
        )

        # This URL needs to be processed
        deal_url = deal_btn.get_attribute("href")

        print(f"Deal URL: {deal_url}")

        # Wait until the img element is present
        try:
            image_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body[@class='no-touch']/div[@id='app']/main[@class='App-content']/div[@id='content']/div[@class='DiscussionPage']/div[@class='DiscussionPage-discussion']/header[@class='Hero DiscussionHero DiscussionHero--colored']/div[@class='container']/ul[@class='DiscussionHero-items']/li[@class='item-discussionDealDetails1']/div[@class='cc_custDetailsHeader']/div[@class='cc_custDetailsHeaderLeftBox']/div[@class='cc_discussionHeaderImage']/div[@class='cc_imageFrame']/img[@class='sm_img lazy']"))
            )

            # Get the src attribute
            image_link = image_div.get_attribute("src")

            with open("images/image.jpg", "wb") as f:
                f.write(requests.get(image_link).content)

                print("Downloaded Image!")

        except Exception as e:
            print(f"Something went wrong while downloading the image: {e}")

        try:
            # GET DEAL TITLE

            p_title_div = driver.find_element(
                By.CLASS_NAME, "cc_productDetailTitle")
            p_title_text = p_title_div.text

            data.append(p_title_text)

            # GET PRODUCT MRP & DEAL PRICE

            pricing_div = driver.find_element(
                By.CLASS_NAME, "cc_blockPriceTextMini")
            mrp = pricing_div.text.split()[0].replace("/-", "")
            deal_price = pricing_div.text.split()[1].replace("/-", "")

            data.append(mrp)
            data.append(deal_price)

            # GET DISCOUNT

            discount_div = driver.find_element(
                By.CLASS_NAME, "cc_blockBadgeTextMini")
            discount = discount_div.text

            data.append(discount)

        except Exception as e:
            print(f"This error occurred while scraping product details: {e}")

        try:
            driver.get(deal_url)

            WebDriverWait(driver, 10).until(
                EC.url_changes(deal_url)
            )

            current_url = driver.current_url
            splitted = current_url.split("?")[0]
            addition = "/?tag=stark05-21"
            final_url = splitted + addition

            print(f"Merchant URL: {final_url}")

            data.append(final_url)

            print(data)

        except Exception as e:
            print(f"This went wrong while generating merchant link: {e}")

    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    while True:
        main()
        # Repeat after 5 Minutes
        time.sleep(300)
