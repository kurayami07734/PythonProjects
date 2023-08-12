from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from tabula import read_pdf
from pandas import DataFrame

rollNumbers = [i for i in range(21117001, 21117130)]
sliders = [i for i in range(21117901, 21117920)]
rollNumbers.extend(sliders)
resultsData = {}


def find_file_url(rollNumber: int) -> tuple[str, str]:
    opts = Options()
    opts.add_argument("-headless")
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
        Select(sessionMenu).select_by_value('104')

        semMenu = wait.until(
            EC.presence_of_element_located((By.ID, "ddlSemester")))

        Select(semMenu).select_by_value('4')

        main_window = browser.current_window_handle

        wait.until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "btnCBCSTabulation"))).click()
        for handle in browser.window_handles:
            if handle != main_window:
                browser.switch_to.window(handle)
                wait.until(EC.url_changes("about:blank"))
                file_url = browser.current_url
                browser.quit()
                print(f'{name} : {file_url} found')
                return (name, file_url)

    except Exception as e:
        browser.quit()
        return ("Does Not Exist", str(e))


def scrapePDF(nameAndURL: tuple[str, str], rollNumber: int):
    if nameAndURL[0] == 'Does Not Exist':
        resultsData[rollNumber] = {
            "Name": nameAndURL[0], "Error": nameAndURL[1][:15]}
        return
    try:
        df = read_pdf(nameAndURL[1],
                      area=(130, 47, 220, 565), pages=1)[0]
        subjects = df['Name of Subjects'].to_list()
        grades = df["Grade Point"].to_list()
        d = zip(subjects, grades)
        pointerArea = read_pdf(
            nameAndURL[1], area=(237, 100, 260, 450), pages=1)[0].columns.values.tolist()
        if "Offer Credit" not in pointerArea[0]:
            ptrs = [ptr.split(":")[1]
                    for ptr in pointerArea]
            if isNumber(ptrs[0]) and isNumber(ptrs[1]):
                ptrs = [float(ptrs[0]), float(ptrs[1])]
            if ptrs[0] > 10 or ptrs[1] > 10:
                data = {'SPI': 'F', 'CPI': 'F',
                        "Name": nameAndURL[0], "URL": nameAndURL[1], "Error": "None"}
            else:
                data = {'SPI': ptrs[0], 'CPI': ptrs[1],
                        "Name": nameAndURL[0], "URL": nameAndURL[1], "Error": "None"}
        else:
            data = {'SPI': 'F', 'CPI': 'F',
                    "Name": nameAndURL[0], "URL": nameAndURL[1], "Error": "None"}
        for sub, grd in d:
            data[sub] = grd
        resultsData[rollNumber] = data
        print(f'{len(resultsData)} {rollNumber} : {resultsData[rollNumber]}')

    except Exception as e:
        print(f"{rollNumber} : {str(e)}")


def isNumber(num: str) -> bool:
    try:
        float(num)
    except ValueError:
        return False
    return True


def fetchResults(rollNumber: int):
    scrapePDF(find_file_url(rollNumber), rollNumber)


def main():
    with ThreadPoolExecutor() as executor:
        executor.map(fetchResults, rollNumbers)
    # fetchResults(20117011)
    # scrapePDF(("CHIRAG GAJBHIYE", "https://mis.nitrr.ac.in/Reports/commonreportForCBCS.aspx?pagetitle=Tabulation_Sheet&path=~,Reports,Academic,rptTabulationRegistarCBCSStud_PubResult.rpt&param=@P_SEMESTER=6,@P_IDNO=16466,@P_SESSIONNO=104,@P_COLLEGE_CODE=53"), 20117023)
    df = DataFrame(resultsData).transpose()
    df.to_csv('results_EE_IV_JUNIORS.csv')
    print(df)


if __name__ == '__main__':
    main()
