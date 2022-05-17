import re
import flair

from pandas import Series, read_json
from typing import List

class Model:
    
    NERtagger = flair.models.SequenceTagger.load('flair/ner-english-ontonotes-large')
    POStagger = flair.models.SequenceTagger.load('flair/upos-english')

    def clean(self, text:Series) -> Series:
        return ( 
            text
            .apply(lambda s: re.sub('<.*>'   , '' , s)) # text enclosed in angle brackets
            .apply(lambda s: re.sub('http\S*', '' , s)) # urls
            .apply(lambda s: re.sub('\s+'    , ' ', s)) # whitespaces
            .apply(lambda s: re.sub('=+|-+'  , '' , s)) # ===.. and ---..
        )


    def predict(self, emails:Series) -> List:

        entitiess  = emails.apply(self.predict_ner)
        pos        = emails.apply(self.predict_pos)

        verbss = pos.apply(
            lambda relations: list(filter(
                lambda relation: 'VERB' == relation['labels']['value'],
                relations
        )))

        objs = verbss + entitiess # collection of entities and verbs

        return entitiess, objs.apply(self.extractRealtions)


    def extractRealtions(self, objs:List) -> List:
        # sorting entities and verbs in the order they appear in the email
        objs = sorted(objs, key= lambda element: element['start_pos'])

        i = 0       # index of first entity
        while i < len(objs) and objs[i]['labels']['value'] == 'VERB': i += 1
        
        j = i + 1   # index of second entity
        while j < len(objs) and objs[j]['labels']['value'] == 'VERB': j += 1
        
        
        temp = []
        while j < len(objs):
            if (objs[j]['start_pos'] - objs[i]['start_pos']) < 30:
                
                temp.append({
                    'entity_A': objs[i],
                    'entity_B': objs[j],
                    'relations': [
                        objs[k]
                        for k in range(i+1,j)
                    ] 
                })
                    
            i = j
            j = j + 1
            while j < len(objs) and objs[j]['labels']['value'] == 'VERB':
                j += 1


        return temp


    def predict_ner(self, email:str) -> List:
        email = flair.data.Sentence(email)

        self.NERtagger.predict(email)

        return list(map(
            lambda entity: {
                **entity,
                'labels': entity['labels'][0].to_dict()
            },
            map(
                lambda spam: spam.to_dict(), 
                email.get_spans()
        )))


    def predict_pos(self, email:str) -> List:
        email = flair.data.Sentence(email)

        self.POStagger.predict(email)

        return list(map(
            lambda entity: {
                **entity,
                'labels': entity['labels'][0].to_dict()
            },
            map(
                lambda spam: spam.to_dict(), 
                email.get_spans()
        )))



if __name__ == '__main__':

    model = Model()

    df = read_json('email/out.json')
    df['cleaned'] = model.clean(df['body'])

    df.to_json('model/out.json', orient= 'records', indent= 4)
    pass