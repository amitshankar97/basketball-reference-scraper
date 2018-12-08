from pymongo import MongoClient
import datetime
import os

client = MongoClient(os.environ['BASKETBALL_DB'])

BASKETBALL = client['basketball']

class DB:
    
    def __init__(self, db=BASKETBALL):
        self.db = db
        self.players = db['players']

    def addOrUpdatePlayer(self, player):
        try:
            player['insertion_time'] = datetime.datetime.utcnow()
            result = self.players.update_one({'_id': player['_id']}, {'$set': player}, upsert=True)
            return result
        except Exception as e:
            return {}

    def getPlayersCollection(self):
        return self.players.find({})

    def getPlayerByName(self, name):
        try:
            return self.players.find_one({'name': name})
        except Exception as e:
            return {}
