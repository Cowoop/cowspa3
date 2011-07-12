import os
import hashlib
from getpass import getpass

def gen_key():
	print('Username:'+os.environ['USER'])
	passwd=getpass('Password:')
	salt='wp45hx'
	h=hashlib.sha256()
	h.update(passwd+salt)
	passwd_encrypt=h.hexdigest()
	print('Encrypted password is=',passwd_encrypt)
gen_key()




















