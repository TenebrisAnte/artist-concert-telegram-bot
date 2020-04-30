import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text

"""Ищет артистов по запросу упаковывает в словарь с ключем имя артиста. Возможно несколько артистов.
Вход: принимает реквест ссылку с поиска (https://www.songkick.com/search?utf8=%E2%9C%93&type=initial&query=)"""
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


# Селектор для выбора одного артиста из словаря
def select_artist():
    pass


"""Парсер для страници артиста
Вход: ссылка на странику артиста и код артиста на сайте"""
def concert(html, artist_link):
    soup = BeautifulSoup(html, "lxml")
    div_inf = soup.find('div', class_ =("col-8 primary artist-overview"))
    tour_inf = div_inf.find('ul').find('li').text.replace("On tour: ", '')
    if tour_inf == "yes":
        r = requests.get(f"https://www.songkick.com/artists/{artist_link}/calendar")
        comp_event = soup.find_all("ol", class_="artist-event-listings")
        #upcoming_conc = comp_event
        return comp_event


def main():
    artist_link = "267261-bi2"
    url = "https://www.songkick.com/artists/" + artist_link
    por =concert(get_html(url), artist_link)
    print(por)


if __name__=="__main__":
    main()