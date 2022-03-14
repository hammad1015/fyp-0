import time
import pandas as pd

from email.emailReader  import EmailReader
from model.model        import Model

emailReader = EmailReader()
model       = Model()

while True:
    n = 10
    emails = pd.DataFrame([
        emailReader.fetchEmail(i)
        for i in range(n)
    ])

    emails['body'  ] = model.clean(emails['body'])
    emails['labels'] = model.predict(emails)

    print(emails)
    
    time.sleep(60)
