import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return soup

"""
Ищет артистов по запросу упаковывает в словарь с ключем имя артиста. Возможно несколько артистов.
вход имя (если несколько слов то зменяет " " на "+"
выход { имя артиста [код артиста, ссылка на картинку артиста ]
"""
def search_artist(name_artist):
    artists_dict = {}
    url = "https://www.songkick.com/search?utf8=%E2%9C%93&type=initial&query=" + name_artist
    soup = get_html(url)
    all_info = soup.find('div', class_="component search event-listings events-summary")
    all_artists = all_info.find_all('li', class_="artist")
    for artist in all_artists:
        name = artist.find("strong").text
        link = artist.find('a', class_= "thumb").get("href")[9:]
        pic = artist.find('img', class_="profile-pic artist").get("src")
        artists_dict[name] = [link, pic]
    return artists_dict




"""
Парсер для страници артиста
Вход: код артиста полученный от бота 
Выход:количество концертов,{сылка на концерт[дата, концертхолл, город_страна(может принимать значение "Canceled" и "POSTPONED")}
"""
def concert(artist_code):
    concert = {}
    url = "https://www.songkick.com/artists/" + artist_code
    soup = get_html(url)
    div_inf = soup.find('div', class_ =("col-8 primary artist-overview"))
    tour_inf = div_inf.find('ul').find('li').text.replace("On tour: ", '')
    if tour_inf == "yes":
        calendar = get_html(url +"/calendar")
        conc_event = calendar.find("div", class_="component events-summary upcoming")
        upcoming_conc = conc_event.find("span", class_="title-copy").text[19:].replace(")", "") # количество предстоящих концертов у артиста
        conc_links = conc_event.find_all("li")
        for conc_link in conc_links:
            link = conc_link.find("a").get("href")
            conc_date = conc_event.find("li", class_="event-listing").get("title")
            conc_place = conc_link.find("strong").text
            conc_hall = conc_link.find("p", class_="secondary-detail").text
            concert[link] = [conc_date, conc_hall, conc_place]
        return upcoming_conc, concert

"""
получить ссылку на покупку билета 
"""

def get_ticket(link_concert):
    url = "https://www.songkick.com/" + link_concert
    soup = get_html(url)
    try:
        ticket_link = soup.find('div', id="tickets").find("a", class_="buy-ticket-link").get("href")
        ticket_vendor = "https://www.songkick.com" + ticket_link
        return ticket_vendor
    except:
        data_search = soup.find("div", class_ ="date-and-name").text.replace("\n", "").replace(" ", "+")
        name_search = soup.find("h1", class_="h0 summary").text.replace("\n", "").replace(" ", "+")
        location_search = soup.find("div", class_="location").text.replace("\n", "").replace(" ", "+").replace(" ", "+")
        google_link =f"https://www.google.com/search?q={data_search}++{name_search}++{location_search}"
        return google_link


"""
Поиск 50 приведущих концертов 
Вход: код артиста полученный от бота 
выход словарь {дата[место проведения, страна ]}
---работает не всегда, еще допиливаю---
"""

def past_concert(artist_code):
    past_concert = {}
    url = (f"https://www.songkick.com/artists/{artist_code}/gigography")
    soup = get_html(url)
    div_inf = soup.find("div", class_="component events-summary")
    ul_inf = div_inf.find("ul", class_="event-listings")
    concerts = ul_inf.find_all("li")
    count = 0
    for concert in concerts:
        count += 1
        if count % 2 == 0:
            conc_date = concert.get("title")
            try:
                conc_place = concert.find("span", class_="venue-name").find("a").text
            except AttributeError:
                conc_place = None
            #conc_city = concert.find("p", "location").find("span", class_=None).text
            past_concert[conc_date] = [conc_place]
    print(past_concert)
    return past_concert




def search_location(location):
    pass





def main():
    artist_code = "4555533-altj"
    print(get_ticket("/concerts/39277247-bi2-at-minsk-arena"))

if __name__=="__main__":
    main()