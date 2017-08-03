import httplib2, os, email, base64, json
import dateutil.parser

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# from models.MailFilterBayseModel import MailFilterBayseModel

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

APP_ROOT   = os.path.dirname(os.path.abspath( __file__ ))
MAIL_DIR   = 'emails'
ATTACHMENT_DIR = 'attachment'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    # labelリストを取得
    results = service.users().messages().list(userId='me', labelIds='Label_15', q='is:unread').execute()
    # results = service.users().messages().list(userId='me', labelIds='Label_15', maxResults=35).execute()
    messages = results.get('messages', [])

    # mail_filter = MailFilterBayseModel()


    for message in messages:
        print(message['id'])

    try:
            # msg_obj = service.users().messages().get(userId='me', id='15da76b21fecf9ee').execute()

            msg_obj = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            email = MailObject(msg_obj['payload'])

            mail_text = email.subject + '\n\n' + email.message
            # result    = mail_filter.calc(mail_text)

            # f = open(os.path.join(APP_ROOT, MAIL_DIR, result[0][0], message['id'] + '.txt'), 'w')
            f = open(os.path.join(APP_ROOT, MAIL_DIR, message['id'] + '.txt'), 'w')
            # f = open(os.path.join(APP_ROOT, MAIL_DIR, 'aaaa.txt'), 'w')
            f.write(mail_text)
            f.close()

            if email.attachment_id:
                data = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=email.attachment_id).execute()
                # for part in data['payload']['parts']:
                #     print("agagagaga", part['filename'])
                #     if part['filename']:
                file_data = base64.urlsafe_b64decode(data['data'].encode('UTF-8'))

                fp = open(os.path.join(APP_ROOT, ATTACHMENT_DIR, email.file_name), 'wb')
                fp.write(file_data)
                fp.close()

            #既読
            service.users().messages() \
                .modify(userId='me', id=message['id'], body={"removeLabelIds": ['UNREAD']}).execute()

            print('===========================================================')
            print('subject : ', email.subject)
            print('send_date : ', email.send_date)
            print('from_addr : ', email.from_addr)
            print('to_addr : ', email.to_addr)
            print('attachment_id : ', email.attachment_id)
            print('file_name : ', email.file_name)
            print('body    : \n', email.message)
            print('===========================================================')

    except Exception as e:
            print(e)


class MailObject(object):
    """
    メールオブジェクト
    """
    subject = ""
    message = ""
    from_addr = ""
    to_addr = ""
    send_date = ""
    attachment_id = ""
    file_name = ""

    def __init__(self, payload):
        super(MailObject, self).__init__()
        body = ""
        attachment_id = ""
        file_name = ""

        if 'data' in payload['body']:
            body = payload['body']['data']

        # elif 'parts' in payload:
        #     for part in payload['parts']:
        #         if len(body) == 0 and 'body' in part and 'data' in part['body']:
        #             body = part['body']['data']
        #         elif 'parts' in part:
        #             for subpart in part['parts']:
        #                 if len(body) == 0 and 'body' in subpart and 'data' in subpart['body']:
        #                     body = subpart['body']['data']


        # payloadのmimeTypeで['multipart/mixed']と['text/plain']できりわけがよいかも
        elif 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == "text/plain":
                    # print("text@@@@@@")
                    body = part['body']['data']

                elif part['mimeType'] == "application/octet-stream":
                    # print("attachment_id@@@@@@")
                    attachment_id = part['body']['attachmentId']
                    file_name = part['filename']

                    # attachmentにdataがない時は取得にいく
                    # あるときはdataに格納されているようだs

                elif 'parts' in part:
                    for subpart in part['parts']:
                        if len(body) == 0 and 'body' in subpart and 'data' in subpart['body']:
                            body = subpart['body']['data']


        for item in payload['headers']:
            if item['name'] == 'Subject':
                self.subject = item['value']

            elif item['name'] == 'Date':
                _date = dateutil.parser.parse(item['value'])
                self.send_date = _date.strftime('%Y-%m-%d %H:%M:%S')

            elif item['name'] == 'To':
                self.to_addr = item['value']

            elif item['name'] == 'From':
                self.from_addr = item['value']

        self.file_name = file_name
        self.attachment_id = attachment_id
        self.message = email.message_from_string(base64.urlsafe_b64decode(body).decode('utf-8')).as_string()


if __name__ == '__main__':
    main()