import os
import sys

sys.path.append('.')

import sphc
import fe
import fe.src.pages as pagelib

pathjoin = os.path.join

pubroot = 'pub'
buildroot = 'build'
contribroot = 'fe/contrib'
srcroot = 'fe/src'

contribs = ['js', 'css']

pages = [(pagelib.InvoicingPage, 'invoicing/home'),
         (pagelib.LoginPage, 'login')
        ]

def copydirs(srcs, dst, verbose=False):
    if isinstance(srcs, basestring):
        srcs = [srcs]
    else:
        srcs = list(srcs)
    if not srcs:
        raise Exception("No source specified")
    print "%s -> %s" % (srcs, dst)
    v = verbose and 'v' or ''
    dstdir = os.path.dirname(dst)
    if dstdir and not os.path.exists(dstdir):
        os.makedirs(dstdir)
    srcs = ' '.join(srcs)
    cmd = "/bin/cp -r%s %s %s" % (v, srcs, dst)
    print "Executing ", cmd
    if os.system(cmd) != 0:
        raise Exception("Copying failed: %s" % cmd)

def copy_contribs():
    contribdirs = (pathjoin(contribroot, name) for name in contribs)
    copydirs(contribdirs, pubroot)

def copy_asset_srcs():
    contribdirs = (pathjoin(srcroot, name) for name in contribs)
    copydirs(contribdirs, pubroot)

def build_pages():
    for Page, _path in pages:
        path = os.path.join(pubroot, _path)
        Page().write(path)

def main():
    if not os.path.exists(pubroot):
        os.makedirs(pubroot)
    copy_contribs()
    copy_asset_srcs()
    build_pages()

if __name__ == '__main__':
    main()
