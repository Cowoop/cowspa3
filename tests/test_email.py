# -*- coding: utf-8 -*-
# Simple script to test SMTP configuration

import commontest
import be.bootstrap
be.bootstrap.start()
import commonlib.messaging

def test_send():
    author = ('Shön', 'shon@example.com') # UTF-8 test
    to = ('Shon', 'launch@cowoop.net')
    subject = 'Shön'
    rich = subject
    env.mailer.send(author, to, subject, rich)

if __name__ == '__main__':
    test_send()
