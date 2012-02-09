import turbomail
from turbomail.control import interface
import html2text

class Mailer(object):

    def __init__(self, config):
        self.config = config

    def start(self):
        interface.start(self.config)

    def stop(self):
        interface.stop()

    def send(self, author, to, subject='', rich='', plain='', cc=[], bcc=[], attachment=[]):
        """
        author: Sender. Tuple of strings like (<name>, <email>) or simply email address
        to: tuple for string same as author
        attachment: [<attachment path>, '<name>']
        """
        if not rich and plain:
            msg = turbomail.Message(author, to, subject, cc=cc, bcc=bcc, plain=plain)
        else:
            if not plain:
                plain = html2text.html2text(rich)
            msg = turbomail.Message(author, to, subject, cc=cc, bcc=bcc, rich=rich, plain=plain)
        if attachment:
            msg.attach(*attachment)
        msg.send()
        return True
