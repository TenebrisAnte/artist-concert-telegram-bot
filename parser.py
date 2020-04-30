import requests
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def searth_artist(html):
    artists_dict = {}
    soup = BeautifulSoup(html, "lxml")
    all_info = soup.find('div', class_="component search event-listings events-summary")
    all_artists = all_info.find_all('li', class_="artist")
    for artist in all_artists:
        name = artist.find("strong").text
        link = artist.find('a', class_= "thumb").get("href")
        pic = artist.find('img', class_="profile-pic artist").get("src")
        artists_dict[name] = [link, pic]
    return artists_dict

def search_concert(url):


def main():
    url = "https://www.songkick.com/search?utf8=%E2%9C%93&query=alison"
    por = searth_artist(get_html(url))
    #print(por)
if __name__=="__main__":
    main()