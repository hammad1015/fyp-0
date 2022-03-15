import imaplib
import credentials
import email
import json

from typing import Dict


class EmailReader:

    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(
        user    = credentials.username, 
        password= credentials.password
    )
    imap.select("INBOX")

    readEmails = 0
    
    def fetchEmail(self, emailId:int) -> Dict[str,str]:

        e = self.imap.fetch(f'{emailId+1}', "(RFC822)")[1][0][1]
        e = email.message_from_bytes(e)
        return {
            '_id'    : emailId,
            'from'   : {
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
    

if __name__ == '__main__':
    emailReader = EmailReader()
    n = 10
    emails = [
        emailReader.fetchEmail(i)
        for i in range(n)
    ]
    json.dump(
        emails, 
        fp= open('email/out.json', 'w'),
        indent= 4
    )
    