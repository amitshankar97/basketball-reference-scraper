from twitterscraper import query_tweets
from datetime import date, timedelta
import json
from db import DB
import time

def jsondump(data):
    with open('tweets.json', 'w') as fp:
        json.dump(data, fp)

if __name__ == '__main__':
    t0 = time.time()

    mongo = DB()
    yesterday = date.today() - timedelta(1)
    
    for player in mongo.getPlayersCollection():

        json_tweets = []

        for tweet in query_tweets(player['name'], limit=10, begindate=yesterday):
            tweetDict = tweet.__dict__
            tweetDict['timestamp'] = str(tweetDict['timestamp'])
            json_tweets.append(tweetDict)
        
        player['twitter'] = json_tweets

        mongo.addOrUpdatePlayer(player)

    t1 = time.time()

    print('ran for ' + str(t1 - t0))