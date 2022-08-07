from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

# scrapping top 14000+ anime names and rating from MAL (by popularity)

def main():
    ratings, names = [], []
    for i in range(0, 300, 50):
        url = (
            "https://myanimelist.net/topanime.php?type=bypopularity"
            if i == 0
            else f"https://myanimelist.net/topanime.php?type=bypopularity&limit={i}"
        )
        html_data = requests.get(url).text
        soup = bs(html_data, "html.parser")
        nameElements = soup.find_all("h3", class_="anime_ranking_h3")
        ratingElements = soup.find_all("span", class_="on")
        ratings.extend([rating.text for rating in ratingElements])
        names.extend([elem.text for elem in nameElements])
    data = list(zip(names, ratings))
    a = pd.DataFrame(data, index=range(1, len(data) + 1), columns=["Name", "Rating"])
    a.rename_axis("Ranking", inplace=True)
    print(a)
    a.to_csv("rankings.csv")


if __name__ == "__main__":
    main()
