import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from fractions import Fraction
import math
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

def GetDataFromGame(game_url):
    response = requests.get(game_url)
    game_soup = BeautifulSoup(response.content,'html.parser')
    #addressing if the page is a bundle page, returning null
    bundle_tag = 1
    package_tag = 1
    bundle_tag = game_soup.find('div', attrs={'class':'game_area_purchase_game bundle ds_no_flags'})
    package_tag = game_soup.find('div', attrs={'id':'package_header_container'})
    if bundle_tag or package_tag:
        return np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan
    

    #addressing if the game is a dlc of a main game
    dlc_tag = game_soup.find('div',attrs={'class':'game_area_bubble game_area_dlc_bubble'})
    soundtrack_tag = game_soup.find('div',attrs={'class':'game_area_bubble game_area_soundtrack_bubble '})
    if dlc_tag or soundtrack_tag:
        return np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan

    age_check_tag = game_soup.find('div',attrs={'id':'app_agegate'})
    if age_check_tag:
        #driver = webdriver.Chrome("C:/Users\Or\PycharmProjects\Hello_World/venv\chromedriver.exe")
        #driver.get("https://5emagic.shop/generate")
        return np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan

    preorder_tag = game_soup.find('div',attrs={'class':'game_area_comingsoon game_area_bubble'})
    if preorder_tag:
        return np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan

    if game_soup.title.string == 'Welcome to Steam':
        return np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan
    game_name = game_soup.find('div',attrs={'class':'apphub_AppName'}).string.strip()
    try:
        game_date = game_soup.find('div',attrs={'class':'date'}).string.strip()
    except:
        game_date = np.nan
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
    game_review_count = int(game_review_count)

    #getting pos review num and cleaning data
    game_review_positive = game_soup.find('label',attrs={'for':'review_type_positive'}).find('span',attrs={'class':'user_reviews_count'}).string.strip()
    game_review_positive = game_review_positive.replace(')','').replace('(','')
    game_review_positive = game_review_positive.replace(',','')
    game_review_positive = int(game_review_positive)

    #getting neg review num and cleaning data
    game_review_negative = game_soup.find('label',attrs={'for':'review_type_negative'}).find('span',attrs={'class':'user_reviews_count'}).string.strip()
    game_review_negative = game_review_negative.replace(')', '').replace('(', '')
    game_review_negative = game_review_negative.replace(',','')
    game_review_negative = int(game_review_negative)

    sub_tag = game_soup.find('div',attrs={'class':'game_area_purchase_game_wrapper game_purchase_sub_dropdown'})
    if sub_tag:
        result = game_soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['game_area_purchase_game_wrapper'])
        try:
            game_price = result.find('div',attrs={'class':'game_purchase_price price'}).string.strip()
        except:
            pass
        #checking regular price if game is currently discounted
        try:
            game_price = purchase_tag.find('div',attrs={'class':'discount_original_price'}).string.strip()
        except:
            pass 
    else:
        #getting game price and cleaning data
        purchase_tag = game_soup.find('div',attrs={'id':'game_area_purchase','class':'game_area_purchase'}).find('div',attrs={'class':'game_area_purchase_game_wrapper'})
        #checking regular game price (not discounted)
        try:
            game_price = purchase_tag.find('div',attrs={'class':'game_purchase_price price'}).string.strip()
        except:
            pass
        #checking regular price if game is currently discounted
        try:
            game_price = purchase_tag.find('div',attrs={'class':'discount_original_price'}).string.strip()
        except:
            pass

    # if price is free to play, set it to 0
    if game_price == 'Free to Play':
        game_price = 0

    #clean price data
    else:
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

    for i in range(1,1000):
        print(i)
        links = []
        baseurl = "https://store.steampowered.com/search/?sort_by=Reviews_DESC&filter=topsellers"
        paramater = "&page="+str(i)
        response = requests.get(baseurl+paramater)
        website_soup = BeautifulSoup(response.content,'html.parser')


        for link in website_soup.find('div', attrs={'id': 'search_resultsRows'}).find_all('a'):
            links.append(link['href'])

        for game_url in links:
            curr_game_name, curr_game_date, curr_game_developer, curr_game_pub, curr_game_genre, curr_game_review_count, curr_game_review_positive, curr_game_review_negative, curr_game_price, curr_game_langs, curr_game_dlc, curr_game_mature, curr_game_single = GetDataFromGame(game_url)
            print("last game cleared was",curr_game_name)
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
            
            #to address the nan instances
            if np.isnan(curr_game_review_count):
                result_score = np.nan
            else:
                Review_Score = Fraction(curr_game_review_positive,curr_game_review_count)
                result_score = Review_Score - ((Review_Score - 0.5)*(2**(-(math.log10(curr_game_review_count + 1)))))
            game_score_list.append(result_score)



    GameDF = pd.DataFrame({'Name':game_name_list,'Date':game_date_list,'Developer':game_developer_list,'Publisher':game_game_publisher_list,'Genre':game_genre_list,'Price':game_price_list,'Langs':game_langs_list,'DLC':game_dlc_flag_list,'Mature':game_mature_flag_list,'Single':game_single_flag_list,'Score':game_score_list})
    print(GameDF.head())
    print(GameDF.shape)
    df.to_csv('SteamGamesDF.csv',index=False)
