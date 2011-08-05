import os
import sys

sys.path.append('.')

import sphc
import fe
import fe.src.pages as pagelib

pubroot = 'pub'
buildroot = 'build'

pages = [(pagelib.InvoicingPage, 'invoicing/home')]

def build_pages():
    for Page, _path in pages:
        path = os.path.join(pubroot, _path)
        Page().write(path)

def main():
    build_pages()

if __name__ == '__main__':
    main()
