import flair
import texthero
from pandas import Series

class Model:
    
    NERtagger = flair.models.SequenceTagger.load('flair/ner-english-ontonotes-large')

    def clean(self, text:Series) -> Series:
        text = texthero.remove_urls(text)
        text = texthero.remove_punctuations(text)

        return text

    
    def predict(self, emails:Series) -> Series:
        emails = emails.apply(flair.data.Sentence)
        emails.apply(self.NERtagger.predict)

        return emails.apply(lambda sentence: [
            span.to_dict()['labels'][0].to_dict()  
            for span in sentence.get_span()
        ])
