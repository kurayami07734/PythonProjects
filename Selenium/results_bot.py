from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import tabula
import pandas as pd
from roll_numbers import *

resultsData = {}


def find_file_url(rollNumber: int) -> str:
    opts = Options()
    # opts.headless = True
    browser = webdriver.Firefox(options=opts)
    wait = WebDriverWait(browser, 20)
    browser.get("https://mis.nitrr.ac.in/publishedresult.aspx")

    numberBox = browser.find_element(By.ID, "txtRegno")
    numberBox.send_keys(rollNumber)
    numberBox.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.ID, "lblSRollNo")))

    sessionMenu = wait.until(
        EC.presence_of_element_located((By.ID, "ddlSession")))
    Select(sessionMenu).select_by_value('102')

    semMenu = wait.until(
        EC.presence_of_element_located((By.ID, "ddlSemester")))
    # semMenu = browser.find_element(By.ID, "ddlSemester")
    # wait.until(EC.presence_of_element_located(By.)
    Select(semMenu).select_by_value('5')

    main_window = browser.current_window_handle

    wait.until(
        EC.element_to_be_clickable(browser.find_element(By.ID, "btnCBCSTabulation"))).click()
    for handle in browser.window_handles:
        if handle != main_window:
            browser.switch_to.window(handle)
            wait.until(EC.url_changes("about:blank"))
            file_url = browser.current_url
            browser.quit()
            return file_url


def scrapePDF(file_url: str, rollNumber: int):
    df = tabula.read_pdf(file_url,
                         area=(130, 47, 260, 565), pages=1)[0]
    subjects = df['Name of Subjects'].to_list()
    grades = df["Grade Point"].to_list()
    d = zip(subjects, grades)
    ptrs = [ptr.split(":")[1] for ptr in tabula.read_pdf(
        file_url, area=(250, 100, 268, 450), pages=1)[0].columns.values.tolist()]
    data = {'SPI': ptrs[0], 'CPI': ptrs[1]}
    for sub, grd in d:
        data[sub] = grd
    resultsData[rollNumber] = data
    print(f'{rollNumber} : {resultsData[rollNumber]}')


def fetchResults(rollNumber: int):
    scrapePDF(file_url=find_file_url(
        rollNumber=rollNumber), rollNumber=rollNumber)


def main():
    remaining = [x for x in rollNumbers if x not in set(done)]
    print(remaining)
    # fetchResults(rollNumber=20117048)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(fetchResults, remaining)

    df = pd.DataFrame(resultsData).transpose()
    df.to_csv('results.csv')
    print(df)


if __name__ == '__main__':
    main()
