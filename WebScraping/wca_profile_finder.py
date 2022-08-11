from requests import get as req
from bs4 import BeautifulSoup as bs

def main():
    name = str("Enter name of speedcuber: ")
    search_url = f'https://www.worldcubeassociation.org/search?q={name}'
    search_page = req.get(search_url).text
    soup = bs(search_page, "html.parser")
    wca_id = soup.select(".wca-id")[0].text
    profile_url = f'https://www.worldcubeassociation.org/persons/{wca_id}'
    soup = bs(req.get(profile_url, "html.parser"))
    # three = (soup.select(".333-event > a").text, 


if __name__ == '__main__':
    main()
