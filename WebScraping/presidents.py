from requests import get
from bs4 import BeautifulSoup as bs

def main():
    url = "https://presidentofindia.nic.in/former-presidents.htm"
    soup = bs(get(url).text, "html.parser")
    names = [name.text for name in soup.select(".presidentListing > h3")]
    tenures = [tenure.text.removeprefix("Term of Office: ") for tenure in soup.select(".presidentListing > h3 + p")]
    print(list(zip(names, tenures)))


if __name__ == "__main__":
    main()
