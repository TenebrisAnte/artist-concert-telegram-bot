import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text

"""
Ищет артистов по запросу упаковывает в словарь с ключем имя артиста. Возможно несколько артистов.
Вход: принимает реквест ссылку с поиска (https://www.songkick.com/search?utf8=%E2%9C%93&type=initial&query=код артиста)
"""
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


"""
Ищет города по запросу упаковывает в словарь Возможно несколько городов.
Вход: принимает реквест ссылку с поиска (https://www.songkick.com/search?page=1&per_page=10&query={ГОРОД}&type=locations)
Вывод: словарь локация: сылка
"""
def searth_location(html):
    location_dict = {}
    soup = BeautifulSoup(html, "lxml")
    all_info = soup.find('div', class_="col-8 primary")
    all_locations =all_info.find("ul").find_all("li", class_="small-city")
    for location in all_locations:
        name = location.find("strong").text
        link = location.find('a').get("href")
        location_dict[name] = link
    return location_dict


# Селектор для выбора одного артиста из словаря
def select_artist():
    pass


"""Парсер для страници артиста
Вход: ссылка на странику артиста и код артиста на сайте
Выход: {сылка на концерт[дата, концертхолл, (город_страна(может принимать значение "Canceled")]"""
def concert(html, artist_link):
    concert = {}
    soup = BeautifulSoup(html, "lxml")
    div_inf = soup.find('div', class_ =("col-8 primary artist-overview"))
    tour_inf = div_inf.find('ul').find('li').text.replace("On tour: ", '')
    if tour_inf == "yes":
        calendar_link = get_html(f"https://www.songkick.com/artists/{artist_link}/calendar")
        calendar = BeautifulSoup(calendar_link, "lxml")
        conc_event = calendar.find("div", class_="component events-summary upcoming")
        upcoming_conc = conc_event.find("span", class_="title-copy").text[19:].replace(")", "") # количество предстоящих концертов у артиста
        conc_links = conc_event.find_all("li")
        for conc_link in conc_links:
            link = conc_link.find("a").get("href")
            conc_date = conc_event.find("li", class_="event-listing").get("title")
            conc_place = conc_link.find("strong").text
            conc_hall = conc_link.find("p", class_="venue").text
            concert[link] = [conc_date, conc_hall, conc_place]
        return upcoming_conc, concert


"""def past_concert(artist_link):
    gigography_link = get_html(f"https://www.songkick.com/artists/{artist_link}/gigography")
    gigography = BeautifulSoup(gigography_link, "lxml")
    return gigography"""

"""
поиск концертов по локации
"""
def location_concert(html):
    pass

def main():
    artist_link = "4769598-alison-wonderland"
    url = "https://www.songkick.com/search?page=1&per_page=10&query=kiev&type=locations"
    por = searth_location(get_html(url))
    print((por))


if __name__=="__main__":
    main()