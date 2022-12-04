from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import tabula
from pandas import DataFrame as df
from roll_numbers import rollNumbers

resultsData = df(columns=['roll Number', "SPI", "CPI"], dtype=float)

for rollNumber in rollNumbers:
    opts = Options()
    # opts.headless = True
    browser = webdriver.Firefox(options=opts)
    browser.get("https://mis.nitrr.ac.in/iitmsoBF2zO1QWoLeV7wV7kw7kcHJeahVjzN4t6MFMeyhUykpKfBA9V+F0/3m6SMOr7hf?enc=2vjcaEnhmvfs4iwSJr18eQaN1iwTCkDZLg4FpnIV12/vTB0HoHDs8kZdmyK5DB9t")

    numberBox = browser.find_element(By.ID, "txtRegno")
    numberBox.send_keys(rollNumber)
    numberBox.send_keys(Keys.RETURN)

    semMenu = WebDriverWait(browser, 2).until(
        EC.presence_of_element_located((By.ID, "ddlSemester")))
    # semMenu = browser.find_element(By.ID, "ddlSemester")
    Select(semMenu).select_by_value('4')
    main_window = browser.current_window_handle
    getResult = browser.find_element(By.ID, "btnCBCSTabulation")
    sleep(2)
    getResult.click()
    for handle in browser.window_handles:
        if handle != main_window:
            browser.switch_to.window(handle)
            sleep(2)
            data = [float(ptr.split(":")[1]) for ptr in tabula.read_pdf(
                browser.current_url, area=(250, 100, 268, 450), pages=1)[0].columns.values.tolist()]
            data.insert(0, rollNumber)
            print(data)
            resultsData.add(data)
    browser.quit()

resultsData.to_csv("result.csv")