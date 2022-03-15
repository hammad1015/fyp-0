import re
import flair

from pandas import Series, read_json


class Model:
    
    NERtagger = flair.models.SequenceTagger.load('flair/ner-english-ontonotes-large')

    def clean(self, text:Series) -> Series:
        return ( 
            text
            .apply(lambda s: re.sub('<.*>'   , '' , s))
            .apply(lambda s: re.sub('http\S*', '' , s))
            .apply(lambda s: re.sub('\s+'    , ' ', s))
            .apply(lambda s: re.sub('=+|-+'  , '' , s))
        )


    
    def predict(self, emails:Series) -> Series:
        emails = emails.apply(flair.data.Sentence)
        emails.apply(self.NERtagger.predict)

        return emails.apply(lambda sentence: [
            span.to_dict()['labels'][0].to_dict()  
            for span in sentence.get_span()
        ])


if __name__ == '__main__':

    model = Model()

    df = read_json('email/out.json')
    df['cleaned'] = model.clean(df['body'])

    df.to_json('model/out.json', orient= 'records', indent= 4)
    pass