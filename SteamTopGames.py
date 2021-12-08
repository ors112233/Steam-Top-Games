
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math



if __name__ == '__main__':

    response = requests.get('https://steam250.com/top250')
    website_soup = BeautifulSoup(response.content, 'html.parser')
    table = website_soup.find('div', attrs={'class':'col1 main ranking'})
    game_name = []
    game_id = []
    game_date = []
    game_genre = []
    game_price = []
    game_score = []
    game_rating = []
    game_votes = []

    for i in range(1,251):
        #finding the i'th row in the table of games
        curr_game = table.find('div', attrs={'id':str(i)})
        #finding all the paramaters of the game
        try:
            curr_game_name = curr_game.find('span', attrs={'class':'title'}).find('a').string.strip()
        except Exception as e:
            print('there is a problem on line' + str(i) + ' cant find name')
            print(e)
            curr_game_name = math.nan
        try:
            curr_game_date = curr_game.find('span', attrs={'class':'date'}).find('a').string.strip()
        except Exception as e:
            print('there is a problem on line' + str(i) + ' cant find date')
            print(e)
            curr_game_date = math.nan
        try:
            curr_game_genre = curr_game.find('a', attrs={'class':'genre'}).string.strip()
        except Exception as e:
            print('there is a problem on line' + str(i)+ ' cant find genre')
            print(e)
            curr_game_genre = math.nan
        try:
            curr_game_price = curr_game.find('span',attrs={'class':'price'}).string.strip()
            curr_game_price = curr_game_price.replace("$", "")
            curr_game_price = float(curr_game_price)
        except Exception as e:
            print('there is a problem on line' + str(i)+ ' cant find price')
            print(e)
            curr_game_price = math.nan
        try:
            curr_game_score = curr_game.find('span', attrs={'class':'score'}).string.strip()
            curr_game_score = float(curr_game_score)
        except Exception as e:
            print('there is a problem on line' + str(i) + ' cant find score')
            print(e)
            curr_game_score = math.nan
        try:
            curr_game_rating = curr_game.find('span', attrs={'class': 'rating'}).string.strip()
            curr_game_rating = curr_game_rating.replace("%","")
            curr_game_rating = float(curr_game_rating)
        except Exception as e:
            print('there is a problem on line' + str(i) +' cant find rating')
            print(e)
            curr_game_rating = math.nan
        try:
            curr_game_votes = curr_game.find('span',attrs={'class':'votes'}).string.strip()
            curr_game_votes = curr_game_votes.replace("votes","")
            curr_game_votes = curr_game_votes.replace(",","")
            curr_game_votes.strip()
            curr_game_votes = float(curr_game_votes)
        except Exception as e:
            print('there is a problem on line' + str(i)+ ' cant find votes')
            print(e)
            curr_game_votes = math.nan
        try:
            curr_game_id = curr_game.find('span',attrs={'class':'title'}).find('a').get('href')
            reversed_id = ""
            for c in curr_game_id[::-1]:
                if c!= "/":
                    reversed_id = reversed_id + c
                else:
                    break
            curr_game_id = ""
            for c in reversed_id[::-1]:
                curr_game_id = curr_game_id+c
        except Exception as e:
            print('there is a problem on line' + str(i)+ ' cant find Id')
            print(e)
            curr_game_id = math.nan

        #appending the paramaters into thier respective lists
        game_name.append(curr_game_name)
        game_date.append(curr_game_date)
        game_genre.append(curr_game_genre)
        game_price.append(curr_game_price)
        game_score.append(curr_game_score)
        game_rating.append(curr_game_rating)
        game_votes.append(curr_game_votes)
        game_id.append(curr_game_id)

    games_df = pd.DataFrame({'Name':game_name,'Date':game_date,'Genre':game_genre,'Price':game_price,'Score':game_score,'Rating':game_rating,'Votes':game_votes})
    print(games_df.info())

