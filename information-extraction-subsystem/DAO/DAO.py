import pymongo

class DAO:

    def __init__(self) -> None:

        client = pymongo.MongoClient("mongodb://localhost:27017/")

        self.db = client['mailex']
        # users = db['users']
        
        self.emails     = self.db['emails']
        self.readEmails = self.db['readEmails']

        # self.emails.drop()
        # self.readEmails.drop()
        # self.readEmails.insert_one({
        #     '_id': 0,
        #     'n'  : 0
        # })

    def getNumReadEmails(self):
        return self.readEmails.find_one(0)['n']

    def setNumReadEmails(self, n:int):
        self.readEmails.update_one(
            {'_id': 0},
            {'$set': {'n': n}}
        )
        
    def insertEmails(self, emails:list):
        self.emails.insert_many(emails)

