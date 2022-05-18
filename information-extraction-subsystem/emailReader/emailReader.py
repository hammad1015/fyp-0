import imaplib
import emailReader.credentials
import email

from typing import Dict, List


class EmailReader:
    
    def fetchEmail(self, emailId:int) -> Dict[str,str]:

        e = self.imap.fetch(f'{emailId+1}', "(RFC822)")[1][0][1]
        e = email.message_from_bytes(e)
        return {
            '_id'    : emailId,
            'date'   : e['Date'],
            'from_'   : {
                'name'         : e['From'].split('<')[ 0].strip(),
                'emailAddress' : e['From'].split('<')[~0][:~0]
            },
            'subject': e['Subject'],
            'body'   : ''.join(
                map     (lambda part: part.get_payload(decode= True).decode(),
                filter  (lambda part: part.get_content_type() == 'text/plain', 
                e.get_payload()
            )))
        }

    def fetchEmails(self, i:int, j:int) -> List:
        i = int(i)
        j = int(j)
        
        return [
            self.fetchEmail(k)
            for k in range(i,j)
        ]

    def getTotalEmails(self):
        return int(self.imap.select("INBOX")[1][0])

    def login(self):
        self.imap = imaplib.IMAP4_SSL('imap.gmail.com')
        self.imap.login(
            user    = emailReader.credentials.username, 
            password= emailReader.credentials.password
        )
        self.imap.select("INBOX")

    def logout(self):
        self.imap.close()
        self.imap.logout()

