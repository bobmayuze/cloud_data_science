#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup
from bs4 import NavigableString,Tag
import pandas as pd 
import requests
import time
import pymongo


from boardgamegeek import BGGClient


db_connection = pymongo.MongoClient("mongodb://application_user:application_user_pass@mongo_result_backend:27017/?authSource=TMS_DB",connect=False)
db = db_connection['TMS_DB']['game_data']

def get_game_basic_info(bgg,target_game_id):
    g = bgg.game(game_id=target_game_id)
    result = [g.year, g.categories, g.mechanics, g.families]
    return(result)



def get_row_info(target_row):
    counter = 0
    for child in target_row.children:

        if isinstance(child, NavigableString): 
            continue
        if counter == 0: # Get rank
            try:
                x = child.findChildren(["a"] , recursive=False)
                game_rank = child.findChildren(["a"] , recursive=False)[0]['name']
            except:
                game_rank = -1
        if counter == 1: # Get game id
            x = child.findChildren(["a"] , recursive=False)
            herf = child.findChildren(["a"] , recursive=False)[0]['href']
            game_id = herf.split('/')[2]
            game_name = herf.split('/')[3]
        if counter == 2: # Get game name        
            pass
        if counter == 3: # Get geek rating        
            geek_rating = child.contents[0].strip()
        if counter == 4: # Get avg rating        
            avg_rating = child.contents[0].strip()
        if counter == 5: # Get vote numbers
            vote_numbers = child.contents[0].strip()
        counter += 1
    result = [game_rank,game_id, game_name, geek_rating, avg_rating, vote_numbers]
    return result



def get_game_page_csv(page_number):
    bgg = BGGClient()
    response = requests.get('https://boardgamegeek.com/browse/boardgame/page/' + str(page_number))
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    item_table = soup.find("div", {"id": "collection"}).find("table",{"id":"collectionitems"})
    rows = item_table.findChildren([ 'tr'])

    data = []
    for index, row in enumerate(rows[1:]):
        current_game_id = get_row_info(row)[1]
        if db.count_documents({"game_id": str(current_game_id)}) >= 1:
            continue
        try :
            current_game_info = get_row_info(row) + get_game_basic_info(bgg,current_game_id)
            print(current_game_info)
            db.insert_one({
                'game_rank' : current_game_info[0] ,
                'game_id' : current_game_info[1],
                'game_name' : current_game_info[2],
                'geek_rating' : current_game_info[3],
                'avg_rating' : current_game_info[4],
                'vote_numbers' : current_game_info[5],
                'year' : current_game_info[6],
                'categories' : current_game_info[7],
                'mechanics' : current_game_info[8],
                'families' : current_game_info[9],
            })
        except Exception as e:
            print(e)

#     time.sleep(120)



def rapper_get_page_csv(i):
    print("Getting page",i)
    get_game_page_csv(i)
    return ("Page Number: {}".format(i))

