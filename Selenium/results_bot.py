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

resultsData = []

for rollNumber in rollNumbers:
    opts = Options()
    # opts.headless = True
    browser = webdriver.Firefox(options=opts)
    wait = WebDriverWait(browser, 20)
    browser.get("https://mis.nitrr.ac.in/iitmsoBF2zO1QWoLeV7wV7kw7kcHJeahVjzN4t6MFMeyhUykpKfBA9V+F0/3m6SMOr7hf?enc=2vjcaEnhmvfs4iwSJr18eQaN1iwTCkDZLg4FpnIV12/vTB0HoHDs8kZdmyK5DB9t")

    numberBox = browser.find_element(By.ID, "txtRegno")
    numberBox.send_keys(rollNumber)
    numberBox.send_keys(Keys.RETURN)

    semMenu = wait.until(
        EC.presence_of_element_located((By.ID, "ddlSemester")))
    # semMenu = browser.find_element(By.ID, "ddlSemester")
    Select(semMenu).select_by_value('4')
    main_window = browser.current_window_handle

    getResult = wait.until(
        EC.element_to_be_clickable(browser.find_element(By.ID, "btnCBCSTabulation"))).click()
    for handle in browser.window_handles:
        if handle != main_window:
            browser.switch_to.window(handle)
            wait.until(EC.url_changes("about:blank"))
            data = [float(ptr.split(":")[1]) for ptr in tabula.read_pdf(
                browser.current_url, area=(250, 100, 268, 450), pages=1)[0].columns.values.tolist()]
            data.insert(0, rollNumber)
            print(data)
            resultsData.append(data)
    browser.quit()

dataframe = df(resultsData, columns=["Roll Number", "SPI", "CPI"])
dataframe.to_csv("result.csv")
