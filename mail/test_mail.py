import httplib2, os, email, base64, json, sys
import dateutil.parser
import textwrap

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
    results = service.users().messages().list(userId='me', labelIds='Label_15', maxResults=10).execute()
    messages = results.get('messages', [])

    # mail_filter = MailFilterBayseModel()

    i = 0

    for message in messages:
        print(message['id'])

        try:
                # msg_obj = service.users().messages().get(userId='me', id='15dee282252fac62').execute()

                # print("これは{}回目". format(i))

                msg_obj = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                # msg_obj = service.users().messages().get(userId='me', id='15dac11af669c765', format='full').execute()

                # print("--payload---", msg_obj['payload'])
                # print("---parts---", msg_obj['payload']['parts'])
                # print("---body---", msg_obj['payload']['body'])
                # print("---header---", msg_obj['payload']['headers'])
                # exit()

                email = MailObject(msg_obj['payload'], message['id'])
                # email = MailObject(msg_obj['payload'], '15dee282252fac62')
                email.set_messages()

                # mailの情報を文の頭につける
                _message_header = "__start_mail_header__" + '\n'
                _message_header += textwrap.dedent(f"""
                    Subject:{email.subject}
                    Sender:{email.sender}
                    SendDate:{email.send_date}
                """).strip()

                if email.file_count is not 0:
                    _message_header += '\n\n' + f"FileCount:{email.file_count}" + '\n'

                    for index, filename in enumerate(email.attachment):

                        mime = email.mime_type.__getitem__(index)
                        filename = email.attachment.__getitem__(index)

                        _message_header += f"File{index + 1}[MimeType:{mime} FileName:{filename}]" + '\n'

                _message_header += "__end_mail_header__"
                mail_text = _message_header + '\n\n' + email.body

                # result    = mail_filter.calc(mail_text)

                mail_dir = os.path.join(APP_ROOT, MAIL_DIR)

                if not os.path.exists(mail_dir):
                    os.makedirs(mail_dir)

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
                print('from_addr : ', email.sender)
                print('file_name : ', email.attachment)
                print('body    : \n', email.body)
                print('===========================================================')

        except Exception as e:
                print(e)


class MailObject(object):
    """
    メールオブジェクト
    """

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, input_subject):
        self.__subject = input_subject

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, input_body):
        self.__body = input_body

    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self, input_sender):
        self.__sender = input_sender

    @property
    def send_date(self):
        return self.__send_date

    @send_date.setter
    def send_date(self, input_date):
        self.__send_date = input_date

    @property
    def attachment(self):
        return self.__attachment

    @attachment.setter
    def attachment(self, input_attachment):
        self.__attachment.append(input_attachment)

    @property
    def mime_type(self):
        return self.__mime_type

    @mime_type.setter
    def mime_type(self, val):
        self.__mime_type.append(val)

    @property
    def file_count(self):
        return len(self.attachment)

    def __init__(self, payload, message_id):
        super(MailObject, self).__init__()
        self.__message_id = message_id
        self.__tmp_headers = payload['headers']
        self.__tmp_body = payload['body']

        # property
        self.__subject = None
        self.__body = None
        self.__sender = None
        self.__send_date = None
        self.__attachment = []
        self.__mime_type = []

        if self.__tmp_body['size'] is 0:
            self.__tmp_parts = payload['parts']

    def set_messages(self):
        self.__set_parts()
        self.__set_headers()

    def __set_parts(self):
        print("__set_parts start \n")
        _raw_body = ""
        if self.__tmp_body['size'] == 0:
            """
                body.sizeが0の時はpartの中にデータがあるはず
            """
            for part in self.__tmp_parts:
                if part["partId"] == '0':
                    # partIdが0のものがメッセージの本文であろう
                    _raw_body = part['body']['data']
                else:
                    # 添付ファイルの数分partがあるはず
                    self.__download_attachment(part)
        else:
            _raw_body = self.__tmp_body['data']

        self.body = email.message_from_string(base64.urlsafe_b64decode(_raw_body).decode('utf-8')).as_string()

    def __set_headers(self):
        print("__set_headers start \n")
        for header in self.__tmp_headers:
            if header['name'] == "Subject":
                self.subject = header['value']

            elif header['name'] == "Date":
                _date = dateutil.parser.parse(header['value'])
                self.send_date = _date.strftime('%Y-%m-%d %H:%M:%S')

            elif header['name'] == "From":
                self.sender = header['value']
        print("__set_headers end \n")

    def __download_attachment(self, part):
        self.mime_type = part["mimeType"]

        if part["filename"]:
            self.attachment.append(part["filename"])
        else:
            _ext = ".txt"
            if self.mime_type is "text/html":
                _ext = ".html"
            _filename = self.__message_id + "_" + part["partId"] + _ext
            self.attachment.append(_filename)

        if "attachmentId" in part["body"]:
            # データを取得しにいく
            _data = self.__get_attachment(part["body"]["attachmentId"])
            _raw_data = _data["data"]

        else:
            _raw_data = part["body"]["data"]

        self.__save_data(_raw_data,
                         self.mime_type.__getitem__((len(self.mime_type)) - 1),
                         self.attachment.__getitem__((len(self.attachment)) - 1)
                         )

    def __get_attachment(self, attId):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        raw_file_data = service.users().messages().attachments() \
            .get(userId='me', messageId=self.__message_id, id=attId).execute()

        return raw_file_data

    def __save_data(self, data, mime, filename):
        mode = "w"

        if mime is not "text/plain":
            mode = "wb"

        attach_dir = os.path.join(APP_ROOT, ATTACHMENT_DIR)

        if not os.path.exists(attach_dir):
            os.makedirs(attach_dir)

        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        with open(os.path.join(APP_ROOT, ATTACHMENT_DIR, filename), mode) as fp:
            fp.write(file_data)

if __name__ == '__main__':
    main()
