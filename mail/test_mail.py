import httplib2, os, email, base64, json, sys
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
    #results = service.users().messages().list(userId='me', labelIds='Label_15', maxResults=10, q='is:unread').execute()
    results = service.users().messages().list(userId='me', labelIds='Label_15', maxResults=50).execute()
    messages = results.get('messages', [])

    # mail_filter = MailFilterBayseModel()


    for message in messages:
        print(message['id'])

    try:
            # msg_obj = service.users().messages().get(userId='me', id='15dac6f3feaaf76f').execute()

            msg_obj = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            # msg_obj = service.users().messages().get(userId='me', id='15dac11af669c765', format='full').execute()

            # print("--payload---", msg_obj['payload'])
            # print("---parts---", msg_obj['payload']['parts'])
            # print("---body---", msg_obj['payload']['body'])
            # print("---header---", msg_obj['payload']['headers'])
            # exit()

            email = MailObject(msg_obj['payload'], message['id'])
            email.set_messages()

            mail_text = email.subject + '\n\n' + email.message
            # result    = mail_filter.calc(mail_text)

            mail_dir = os.path.join(APP_ROOT, MAIL_DIR)

            if not os.path.exists(mail_dir):
                os.mkdirs(mail_dir)

            #####  f = open(os.path.join(APP_ROOT, MAIL_DIR, result[0][0], message['id'] + '.txt'), 'w')
            f = open(os.path.join(APP_ROOT, MAIL_DIR, message['id'] + '.txt'), 'w')
            # f = open(os.path.join(APP_ROOT, MAIL_DIR, 'aaaa.txt'), 'w')
            f.write(mail_text)
            f.close()


            #既読
            service.users().messages() \
                .modify(userId='me', id=message['id'], body={"removeLabelIds": ['UNREAD']}).execute()



            print('===========================================================')
            print('subject : ', email.subject)
            print('send_date : ', email.send_date)
            print('from_addr : ', email.from_addr)
            print('to_addr : ', email.to_addr)
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
    file_name = ""
    mime_type = ""

    def __init__(self, payload, message_id):
        super(MailObject, self).__init__()
        self.__message_id = message_id
        self.__mime_type = payload['mimeType']
        self.__headers = payload['headers']
        self.__body = payload['body']

        if self.__body['size'] == 0:
            self.__parts = payload['parts']

    def set_messages(self):
        self.__set_parts()
        self.__set_headers()

    def __set_parts(self):
        print("__set_parts start \n")
        raw_message = ""
        if self.__body['size'] == 0:
            """
                body.sizeが0の時はpartの中にデータがあるはず
            """
            for part in self.__parts:
                if part["partId"] == '0':
                    # partIdが0のものがメッセージの本文であろう
                    raw_message = part['body']['data']
                else:
                    # 添付ファイルの数分partがあるはず
                    self.__download_attachment(part)
        else:
            raw_message = self.__body['data']

        self.message = email.message_from_string(base64.urlsafe_b64decode(raw_message).decode('utf-8')).as_string()

    def __set_headers(self):
        print("__set_headers start \n")
        for header in self.__headers:
            if header['name'] == "Subject":
                self.subject = header['value']

            elif header['name'] == "Date":
                _date = dateutil.parser.parse(header['value'])
                self.send_date = _date.strftime('%Y-%m-%d %H:%M:%S')

            elif header['name'] == "To":
                self.to_addr = header['value']

            elif header['name'] == "From":
                self.from_addr = header['value']
        print("__set_headers end \n")

    def __download_attachment(self, part):
        self.mime_type = part["mimeType"]
        if part["filename"]:
            self.file_name = part["filename"]

        else:
            _ext = ".txt"
            if self.mime_type == "text/html":
                _ext = ".html"

            self.file_name = self.__message_id + "_" + part["partId"] + _ext

        if "attachmentId" in part["body"]:
            # データを取得しにいく
            raw_data = self.__get_attachment(part["body"]["attachmentId"])
            self.__save_data(raw_data["data"])

        else:
            self.__save_data(part["body"]["data"])

    def __get_attachment(self, attId):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        raw_file_data = service.users().messages().attachments() \
            .get(userId='me', messageId=self.__message_id, id=attId).execute()

        return raw_file_data

    def __save_data(self, raw_data):
        mode = "w"

        if self.mime_type != "text/plain":
            mode = "wb"

        attach_dir = os.path.join(APP_ROOT, ATTACHMENT_DIR)

        if not os.path.exists(attach_dir):
            os.mkdirs(attach_dir)

        file_data = base64.urlsafe_b64decode(raw_data.encode('UTF-8'))
        with open(os.path.join(APP_ROOT, ATTACHMENT_DIR, self.file_name), mode) as fp:
            fp.write(file_data)

if __name__ == '__main__':
    main()
