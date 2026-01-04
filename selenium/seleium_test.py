from selenium import webdriver

driver = webdriver.Firefox()
try:
    driver.get("http://localhost:5173/")
    print(driver.title)
finally:
    driver.quit()