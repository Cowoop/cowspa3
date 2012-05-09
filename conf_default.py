config = {
    'mode': 'DEV', # Options: DEV, TEST, PROD
    'pgdb': {'database': 'shon'}, # eg. {'database': 'mydb', 'username': 'shon', 'password': 'secret', 'host': 'localhost', 'port': ..}
    'random_str': 'PLEASE_CHANGE',
    'mail': {
        'mail.on': False,
        'mail.transport': 'smtp',
        'mail.smtp.server': 'localhost',
        'mail.smtp.port': 25,
        'mail.smtp.tls': False,
        'mail.smtp.username': '',
        'mail.smtp.password': '',
        'mail.smtp.debug': False,
        'mail.utf8qp.on': True
        },
    'http_baseurl': 'http://127.0.0.1:5000',
    'system_username': 'system',
    'threaded': False,
    'words': {},
    'hostname': '127.0.0.1',
    'port': 5001,
    'conf_mode': 'testing',
}
