import pandas as pd
import cv2
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from Ebay_Scraper import ebay_navigation
import requests
import os
from time import sleep
import undetected_chromedriver as uc


keyword = input("Enter keyword: ")
# keyword = "yankee candles"
# user_profile_path = r'C:\Users\dwdqb\AppData\Local\Google\Chrome\User Data'
# profile_name = "Dawood"
options = uc.ChromeOptions()
# options.add_argument(f"--user-data-dir={user_profile_path}")
# options.add_argument(f"--profile-directory={profile_name}")
options.add_argument("--lang=en")
options.add_argument("--disable-popup-blocking")
driver = uc.Chrome(options=options)
driver.maximize_window()
# sleep(5)

url = 'https://www.walmart.com/'
driver.get(url)
actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)


search = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/span/header/form/div/input')))
search.click()
search.send_keys(keyword)
sleep(1)
actions.send_keys(Keys.ENTER)
actions.perform()
sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(2)
data = []
links = []
driver.execute_script("window.scrollTo(0, 0);")

# Through XPATH
for i in range(1, 12):
    sub_data = []
    if i == 9 or i == 17:
        continue
    # try:
        # Candles one
    try:
        link = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="0"]/section/div/div[{i}]/div/div/a'))).get_attribute("href")
    except:
        try:
            link = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/a'))).get_attribute("href")
        except:
            continue
            # link = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/section/div/a'))).get_attribute("href")

    title = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[2]/span"))).text
    try:
        price_1 = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[2]/div[1]/div/span[3]"))).text
    except:
        # price = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[2]/div/div/div/div/div[2]/div[1]/div/span[3]"))).text
        pass
    try:
        price_2 = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[2]/div[1]/div/span[4]"))).text
    except:
        # price = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[2]/div/div/div/div/div[2]/div[1]/div/span[3]"))).text
        pass
    try:
        price = price_1 + "." + price_2
    except:
        price = "NA"
    try:
        shipping_company = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[2]/div[4]/div"))).text
    except:
        try:
            shipping_company = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[2]/div[5]/div"))).text
        except:
            shipping_company = "Unknown"
    try:
        rating_review = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[2]/div[2]/span[3]"))).text
    except:
        try:
            rating_review = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[2]/div[3]/span[3]"))).text
        except:
            try:
                rating_review = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[2]/div[4]/span[3]"))).text
            except: 
                rating_review = "0"
    if not "0" in rating_review:
        rating = rating_review[:3]
        review = rating_review[-10:-8]
    else:
        review = 0
        rating = 0
    try:
        picture_link = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/div/main/div/div[2]/div/div/div[1]/div[2]/div/section/div/div[{i}]/div/div/div/div/div[1]/div[2]/div[1]/img"))).get_attribute("src")
    except:
        pass
    img_response = requests.get(picture_link)
    img_name = os.path.join(r"C:\Users\dwdqb\Desktop\Python Programs\Drop Shipping\Walmart to Ebay\Walmart_Images", f'image_{i-1}.jpg')
    with open(img_name, 'wb') as file:
        file.write(img_response.content)
    if "Save" in shipping_company:
        shipping_company = "Walmart+"
    if "Free shipping" in shipping_company:
        shipping_company = "Unknown"
    driver.execute_script("window.scrollBy(0, 200);")
    links.append(link)
    try:
        rtng = float(rating)
    except:
        rtng = float(rating.split(" ")[0])
    print("\nLink no.:", len(links))
    print("Title:",title)
    print("Price:",price)
    print("Rating:",rtng)
    print("Reviews:", review)
    print("Company:",shipping_company)
    # print("Shipping time:",difference)
    sub_data.append(title[:65])
    sub_data.append(price)
    sub_data.append(rtng)
    sub_data.append(review)
    sub_data.append(shipping_company)
    sub_data.append(link)
    data.append(sub_data)
df = pd.DataFrame(data, columns=["Title", "Price", "Rating", "Review", "Shipping_Company", "Link"])
df.to_csv(r"C:\Users\dwdqb\Desktop\Python Programs\Drop Shipping\Walmart to Ebay\Walmart_Images\Data.csv")
print("Successfully breached!!!")
for i in range(len(df)):
    print("\n")
    print(df['Title'][i])
    print(data[i][0])
    if float(df['Rating'][i]) < 4.2:
        continue
    soldings = []
    try:
        ebay_navigation(driver, df['Title'][i], i, soldings)
    except:
        continue