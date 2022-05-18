import time
import pandas as pd

from emailReader.emailReader    import EmailReader
from model.model                import Model
from DAO.DAO                    import DAO


emailReader = EmailReader()
model       = Model()
dao         = DAO()

while True:
    emailReader.login()

    totalEmails  = emailReader.getTotalEmails()
    nReadEmails  = dao.getNumReadEmails()
    nTotalEmails = emailReader.getTotalEmails()
    emails       = pd.DataFrame(emailReader.fetchEmails(nReadEmails, nTotalEmails))

    print(f'total: {nTotalEmails} read: {nReadEmails}')

    if not emails.empty:
        emails['body'     ] = model.clean(emails['body'])

        entities, relations = model.predict(emails['body'])

        emails['entities' ] = entities
        emails['relations'] = relations

        dao.insertEmails(emails.to_dict('records'))
        dao.setNumReadEmails(nTotalEmails)
        
        # emails.to_json('out.json', orient= 'records', indent= 4)

    emailReader.logout()
    time.sleep(5)
    print('iteration done')
    # exit()
