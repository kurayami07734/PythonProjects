from selenium import webdriver


def main():
    driver = webdriver.Firefox()
    driver.get("https://www.google.com/")
    print(driver.title)
    driver.quit()


if __name__ == "__main__":
    main()
