import requests
from bs4 import BeautifulSoup
import pandas as pd

def GetDataFromGame(game_url):
    response = requests.get(game_url)
    game_soup = BeautifulSoup(response.content,'html.parser')
    game_name = game_soup.find('div',attrs={'class':'apphub_AppName'}).string.strip()
    game_date = game_soup.find('div',attrs={'class':'date'}).string.strip()
    game_developer = game_soup.find('div',attrs={'id':'developers_list'}).find('a').string.strip()
    game_genre = []
    game_genre_prep = game_soup.find('span',attrs={'data-panel':'{"flow-children":"row"}'}).find_all('a')
    for i in game_genre_prep:
        game_genre.append(i.string.strip())
    game_review_count = game_soup.find('label',attrs={'for':'review_type_all'}).find('span',attrs={'class':'user_reviews_count'}).string.strip()
    game_review_count = game_review_count.replace(')','').replace('(','')
    try:
        game_review_count = game_review_count.replace(',','')
    except Exception as e:
        print(e)
    game_review_count = float(game_review_count)
    game_review_positive = game_soup.find('label',attrs={'for':'review_type_positive'}).find('span',attrs={'class':'user_reviews_count'}).string.strip()
    game_review_positive = game_review_positive.replace(')','').replace('(','')
    try:
        game_review_positive = game_review_positive.replace(',','')
    except Exception as e:
        print(e)
    game_review_positive = float(game_review_positive)
    game_review_negative = game_soup.find('label',attrs={'for':'review_type_negative'}).find('span',attrs={'class':'user_reviews_count'}).string.strip()
    game_review_negative = game_review_negative.replace(')', '').replace('(', '')
    try:
        game_review_negative = game_review_negative.replace(',','')
    except Exception as e:
        print(e)
    game_review_negative = float(game_review_negative)
    game_price = game_soup.find('div',attrs={'class':'game_purchase_price price'}).string.strip()
    game_price = game_price.replace('₪','')
    try:
        game_price = game_price.replace(',','')
    except Exception as e:
        print(e)
    game_price = float(game_price)

    return game_name,game_date,game_developer,game_genre,game_review_count,game_review_positive,game_review_negative,game_price


if __name__ == '__main__':
    baseurl = "https://store.steampowered.com/search/?sort_by=Reviews_DESC&filter=topsellers"
    response = requests.get(baseurl)
    website_soup = BeautifulSoup(response.content, 'html.parser')
    List_of_games_tags = website_soup.find('div', attrs={'id': 'search_resultsRows'}).find_all('a')
    links = []
    game_id = []
    game_name_list = []
    game_date_list = []
    game_developer_list = []
    game_genre_list = []
    game_review_count_list = []
    game_review_positive_list = []
    game_review_negative_list = []
    game_price_list = []
    for i in List_of_games_tags:
        links.append(i.get('href'))
        game_id.append(i.get('data-ds-appid'))
    for game_url in links:
        curr_game_name, curr_game_date, curr_game_developer, curr_game_genre, curr_game_review_count, curr_game_review_positive, curr_game_review_negative, curr_game_price = GetDataFromGame(game_url)
        print("game_url" + game_url + 'succsseded')
        game_name_list.append(curr_game_name)
        game_date_list.append(curr_game_date)
        game_developer_list.append(curr_game_developer)
        game_genre_list.append(curr_game_genre)
        game_review_count_list.append(curr_game_review_count)
        game_review_positive_list.append(curr_game_review_positive)
        game_review_negative_list.append(curr_game_review_negative)
        game_price_list.append(curr_game_price)
    for i in range(50,1000,50):
        baseurl = "https://store.steampowered.com/search/results/"
        paramater = "query&start=" + str(i) + "&count=50&dynamic_data=&sort_by=Reviews_DESC&snr=1_7_7_7000_7&filter=topsellers&infinite=1"
        response = requests.get(baseurl+paramater)
        website_soup = BeautifulSoup(response.content,'html.parser')
        List_of_games_tags = website_soup.find('div',attrs={'id':'search_resultsRows'}).find_all('a')
        for i in List_of_games_tags:
            links.append(i.get('href'))
            game_id.append(i.get('data-ds-appid'))
        for game_url in links:
            curr_game_name,curr_game_date,curr_game_developer,curr_game_genre,curr_game_review_count,curr_game_review_positive,curr_game_review_negative,curr_game_price = GetDataFromGame(game_url)
            game_name_list.append(curr_game_name)
            game_date_list.append(curr_game_date)
            game_developer_list.append(curr_game_developer)
            game_genre_list.append(curr_game_genre)
            game_review_count_list.append(curr_game_review_count)
            game_review_positive_list.append(curr_game_review_positive)
            game_review_negative_list.append(curr_game_review_negative)
            game_price_list.append(curr_game_price)

        GameDF = pd.DataFrame({'Id':game_id,'Name':game_name_list,'Date':game_date_list,'Developer':game_developer_list,'Genre':game_genre_list,'Price':game_price_list,'Review Count':game_review_count_list,'Positive Review Count':game_review_positive_list,'Negative Review Count Review Count':game_review_negative_list})
        print(GameDF.head())