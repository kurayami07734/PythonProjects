from requests import get
from bs4 import BeautifulSoup as bs

def main():
    url = 'https://www.imdb.com/india/top-rated-indian-movies/'
    soup = bs(get(url).text, "html.parser")
    names = [name.text for name in soup.select(".titleColumn > a")]
    releaseYear = [int(year.text.strip(' ()')) for year in soup.select(".secondaryInfo")]
    ratings = [float(rating.text) for rating in soup.select(".imdbRating")]
    print(list(zip(names, releaseYear, ratings)))

if __name__ == "__main__":
    main()