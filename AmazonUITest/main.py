import time
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

service = Service("./chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option(name="detach", value=True)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.amazon.com.tr/")
driver.maximize_window()
wait = WebDriverWait(driver, 10)
#çerezleri kabul et
driver.find_element(By.ID,"sp-cc-accept").click()
#giriş yap
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//a[@data-nav-role='signin']"))
)
driver.find_element(By.XPATH, "//a[@data-nav-role='signin']").click()
driver.find_element(By.ID,"ap_email").send_keys("amazon@gmail.com")
driver.find_element(By.ID,"continue").click()
driver.find_element(By.ID,"ap_password").send_keys("password")
driver.find_element(By.ID, "signInSubmit").click()
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "nav-link-accountList-nav-line-1"))
)
#arama
driver.find_element(By.ID,"searchDropdownBox").send_keys("bilgisayarlar")
driver.find_element(By.ID,"searchDropdownBox").send_keys(Keys.RETURN)
driver.find_element(By.ID,"twotabsearchtextbox").send_keys("msi")
driver.find_element(By.ID,"nav-search-submit-button").click()
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.a-size-base.a-spacing-small.a-spacing-top-small.a-text-normal"))
)
footer = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='2 sayfasına git']")))
print(footer.text)

driver.execute_script("arguments[0].scrollIntoView(true);", footer)
driver.execute_script("arguments[0].click();", footer)

wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']")))
products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(10)
non_sponsored = []

# Sponsorlu olmayan ürünleri listele
for product in products:
    if "Sponsorlu" not in product.text:
        non_sponsored.append(product)

if len(non_sponsored) > 1:
    link = non_sponsored[1].find_element(By.TAG_NAME, "a")
    driver.execute_script("arguments[0].scrollIntoView(true);", link)
    link.click()
else:
    pass
wait = WebDriverWait(driver, 10)
title=wait.until(EC.visibility_of_element_located((By.ID,"productTitle")))
print(title.text)
driver.find_element(By.ID,"add-to-wishlist-button-submit").click()
wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='a-size-medium-plus huc-atwl-header-main']")))
driver.find_element(By.XPATH, "//input[@aria-label='Alışverişe devam et']").click()
#driver.execute_script("window.scrollTo(0, 0);")
accountlist=wait.until(EC.visibility_of_element_located((By.ID,"nav-link-accountList")))
accountlist.click()

element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='nav-text' and text()='Alışveriş Listesi']")))
element.click()
driver.find_element(By.XPATH, "//input[@name='submit.deleteItem' and @type='submit']").click()
deleted=wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='a-alert-content' and text()='Silindi']")))
print(deleted.text)
driver.find_element(By.XPATH, "//button[@aria-label='Hesabı ve listeleri genişletme']").click()
logout= wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='nav-text' and text()='Çıkış Yap']")))
logout.click()



