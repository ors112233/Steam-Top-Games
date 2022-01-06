import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def GetDataFromGame(game_url):
    response = requests.get(game_url)
    game_soup = BeautifulSoup(response.content,'html.parser')
    #addressing if the page is a bundle page, directing to the main game link
    bundle_tag = game_soup.find('div', attrs={'id':'package_header_container'})
    if bundle_tag:
        game_url = game_soup.find('div', attrs={'class':'tab_item tablet_list_item app_impression_tracked'}).find('a')['href']
        response = requests.get(game_url)
        game_soup = BeautifulSoup(response.content,'html.parser')
    
    dlc_tag = game_soup.find('div',attrs={'class':'game_area_bubble game_area_dlc_bubble '})
    game_name = game_soup.find('div',attrs={'class':'apphub_AppName'}).string.strip()
    game_date = game_soup.find('div',attrs={'class':'date'}).string.strip()
    game_developer = game_soup.find('div',attrs={'id':'developers_list'}).find('a').string.strip()
    for pub in game_soup.find('div',attrs={'class':'glance_ctn_responsive_left'}).find_all('div',attrs={'class':'dev_row'}):
        game_publisher = (pub.find('a').string.strip()) #always ends on the 2nd string, which is pub
    game_genre = []
    for i in game_soup.find('span',attrs={'data-panel':'{"flow-children":"row"}'}).find_all('a'):
        game_genre.append(i.string.strip())

    #getting review num and cleaning data
    game_review_count = game_soup.find('label',attrs={'for':'review_type_all'}).find('span',attrs={'class':'user_reviews_count'}).string.strip()
    game_review_count = game_review_count.replace(')','').replace('(','')
    game_review_count = game_review_count.replace(',','')
    game_review_count = float(game_review_count)

    #getting pos review num and cleaning data
    game_review_positive = game_soup.find('label',attrs={'for':'review_type_positive'}).find('span',attrs={'class':'user_reviews_count'}).string.strip()
    game_review_positive = game_review_positive.replace(')','').replace('(','')
    game_review_positive = game_review_positive.replace(',','')
    game_review_positive = float(game_review_positive)

    #getting neg review num and cleaning data
    game_review_negative = game_soup.find('label',attrs={'for':'review_type_negative'}).find('span',attrs={'class':'user_reviews_count'}).string.strip()
    game_review_negative = game_review_negative.replace(')', '').replace('(', '')
    game_review_negative = game_review_negative.replace(',','')
    game_review_negative = float(game_review_negative)

    #getting game price and cleaning data
    game_price = game_soup.find('div',attrs={'class':'game_purchase_price price'}).string.strip()
    game_price = game_price.replace('₪','')
    game_price = game_price.replace(',','')
    game_price = float(game_price)

    game_langs = []
    for lang in game_soup.find('div',attrs={'id':'languageTable'}).find_all('td',attrs={'class':'ellipsis'}):
        game_langs.append(lang.string.strip())

    if game_soup.find('div',attrs={'id':'gameAreaDLCSection'}):
        game_dlc = 1
    else:
        game_dlc = 0

    if game_soup.find('div',attrs={'id':'game_area_content_descriptors'}):
        game_mature = 1
    else:
        game_mature = 0
    
        
    #dealing with very special case where there is no cat_block
    try:
        single_tag = game_soup.find('div',attrs={'id':'category_block'}).find('div',attrs={'class':'label'}).string.strip()
        if single_tag == 'Single-player':
            game_single = 1
        else:
            game_single = 0
    except:
        game_single = np.nan

    return game_name,game_date,game_developer,game_publisher,game_genre,game_review_count,game_review_positive,game_review_negative,game_price,game_langs,game_dlc,game_mature,game_single


if __name__ == '__main__':
    #get of 50 first games
    baseurl = "https://store.steampowered.com/search/?sort_by=Reviews_DESC&filter=topsellers"
    response = requests.get(baseurl)
    website_soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    #finds each game's http link
    for link in website_soup.find('div', attrs={'id': 'search_resultsRows'}).find_all('a'):
        links.append(link['href'])

    #these are the lists that will become the cols of the dataframe:
    game_name_list = []
    game_date_list = []
    game_developer_list = []
    game_publisher_list = []
    game_genres_list = []
    game_price_list = []
    game_langs_list = []
    game_dlc_flag_list = []
    game_mature_flag_list = []
    game_single_flag_list = []
    game_score_list = []

    #these will be used to calc the score of each game:
    game_review_count_list = []
    game_review_positive_list = []
    game_review_negative_list = []
    
    #get each games data and append the respective lists
    for game_url in links:
        curr_game_name, curr_game_date, curr_game_developer, curr_game_pub, curr_game_genre, curr_game_review_count, curr_game_review_positive, curr_game_review_negative, curr_game_price, curr_game_langs, curr_game_dlc, curr_game_mature, curr_game_single = GetDataFromGame(game_url)
        game_name_list.append(curr_game_name)
        game_date_list.append(curr_game_date)
        game_developer_list.append(curr_game_developer)
        game_publisher_list.append(curr_game_pub)
        game_genres_list.append(curr_game_genre)
        game_review_count_list.append(curr_game_review_count)
        game_review_positive_list.append(curr_game_review_positive)
        game_review_negative_list.append(curr_game_review_negative)
        game_price_list.append(curr_game_price)
        game_langs_list.append(curr_game_langs)
        game_dlc_flag_list.append(curr_game_dlc)
        game_mature_flag_list.append(curr_game_mature)
        game_single_flag_list.append(curr_game_single)
    for i in range(50,5100,50):
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
