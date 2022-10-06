from cgitb import html
import requests
import bs4 as bs

def main():
    url = 'https://www.imdb.com/chart/top'
    html_data = requests.get(url).text
    soup = bs.BeautifulSoup(html_data, "html.parser")
    movieNames = [name.text for name in soup.select(".titleColumn > a")]
    releaseYear = [int(year.text.strip('()')) for year in soup.select(".secondaryInfo")]
    print(releaseYear)


if __name__ == "__main__":
    main()