import pymongo

class DAO:
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['mailex']
    # users = db['users']
    emails      = db['emails']
    readEmails  = db['readEmails']

    # emails.drop()

    def getNumReadEmails(self):
        return self.readEmails.find_one()['n']

    def setNumReadEmails(self, n:int):
        self.readEmails.update_one(
            { 
                '_id': 0 
            },{ 
                '$set': { 
                    'n': n 
            }})
        
    def insertEmails(self, emails:list):
        self.emails.insert_many(emails)
