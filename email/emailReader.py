import imaplib
from typing import Dict
import credentials
import email

class EmailReader:

    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(
        user    = credentials.username, 
        password= credentials.password
    )
    imap.select("INBOX")

    readEmails = 0
    
    def fetchEmail(self, emailId:int) -> Dict[str,str]:

        e = self.imap.fetch(f'{emailId}', "(RFC822)")[1][0][1]
        e = email.message_from_bytes(e)
        return {
            'from'   : e['From'],
            'to'     : e['To'],
            'subject': e['Subject'],
            'body'   : ''.join(
                map     (lambda part: part.get_payload(decode= True).decode(),
                filter  (lambda part: part.get_content_type() == 'text/plain', 
                e.get_payload()
            )))
        }
    