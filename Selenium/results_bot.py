from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from tabula import read_pdf
from pandas import DataFrame

rollNumbers = [i for i in range(20117001, 20117130)]
sliders = [i for i in range(20117901, 20117920)]
rollNumbers.extend(sliders)
resultsData = {}


def find_file_url(rollNumber: int) -> tuple[str, str]:
    opts = Options()
    opts.headless = True
    browser = webdriver.Firefox(options=opts)
    browser.set_window_size(1440, 900)
    wait = WebDriverWait(browser, 8)
    browser.get("https://mis.nitrr.ac.in/publishedresult.aspx")

    numberBox = browser.find_element(By.ID, "txtRegno")
    numberBox.send_keys(rollNumber)
    numberBox.send_keys(Keys.RETURN)

    try:
        wait.until(EC.presence_of_element_located((By.ID, "lblSRollNo")))
        name = browser.find_element(By.ID, "lblSName").text

        sessionMenu = wait.until(
            EC.presence_of_element_located((By.ID, "ddlSession")))
        Select(sessionMenu).select_by_value('102')

        semMenu = wait.until(
            EC.presence_of_element_located((By.ID, "ddlSemester")))

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
                return (name, file_url)

    except Exception as e:
        browser.quit()
        return ("Does Not Exist", str(e))


def scrapePDF(nameAndURL: tuple[str, str], rollNumber: int):
    if nameAndURL[0] == 'Does Not Exist':
        resultsData[rollNumber] = {
            "Name": nameAndURL[0], "Error": nameAndURL[1][:15]}
        return
    df = read_pdf(nameAndURL[1],
                  area=(130, 47, 260, 565), pages=1)[0]
    subjects = df['Name of Subjects'].to_list()
    grades = df["Grade Point"].to_list()
    d = zip(subjects, grades)
    ptrs = [float(ptr.split(":")[1]) for ptr in read_pdf(
        nameAndURL[1], area=(250, 100, 268, 450), pages=1)[0].columns.values.tolist()]
    if ptrs[0] > 10 or ptrs[1] > 10:
        data = {'SPI': 'F', 'CPI': 'F', "Name": nameAndURL[0], "Error": "None"}
    else:
        data = {'SPI': ptrs[0], 'CPI': ptrs[1],
                "Name": nameAndURL[0], "Error": "None"}
    for sub, grd in d:
        data[sub] = grd
    resultsData[rollNumber] = data
    print(f'{len(resultsData)} {rollNumber} : {resultsData[rollNumber]}')


def fetchResults(rollNumber: int):
    scrapePDF(find_file_url(rollNumber), rollNumber)


def main():
    # fetchResults(rollNumber=20115050)
    with ThreadPoolExecutor() as executor:
        executor.map(fetchResults, rollNumbers)

    df = DataFrame(resultsData).transpose()
    df.to_csv('results_EE.csv')
    print(df)


if __name__ == '__main__':
    main()
