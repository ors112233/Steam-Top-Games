
import requests
from bs4 import BeautifulSoup



if __name__ == '__main__':

    response = requests.get('https://steam250.com/top250')
    website_soup = BeautifulSoup(response.content, 'html.parser')
    table = website_soup.find('div', attrs={'class':'col1 main ranking'})
    game_name = []
    for i in range(1,251):
        curr_game = table.find('div', attrs={'id':str(i)})
        curr_game_tag = curr_game.find()
        print(curr_game_tag)
        print('============')
        #curr_game_name = curr_game_tag.string.strip()
        #game_name.append(curr_game_name)
    #print(game_name)