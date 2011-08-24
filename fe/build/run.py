import os
import sys
import itertools
import glob

sys.path.append('.')

import sphc
import commonlib.helpers
import fe
import fe.src.pages as pagelib
import fe.src.member_pages as memberlib
import fe.src.bizplace_pages as bizplacelib
import fe.src.plan_pages as planlib
import fe.src.resource_pages as resourcelib

pathjoin = os.path.join

pubroot = 'pub'
buildroot = 'build'
contribroot = 'fe/contrib'
srcroot = 'fe/src'
contribs = ['js', 'css', 'images']
roles = ['host']
themeroot = 'fe/src/themes'
themedirs = [os.path.basename(name) for name in glob.glob(themeroot + '/*') if os.path.isdir(name)]
themedirs.remove('base')
scsscompile_cmd = "/var/lib/gems/1.8/gems/sass-3.1.7/bin/scss %(infile)s %(outfile)s -I `pwd`"

def themedict(themedir):
    manifest_path = pathjoin(themeroot, themedir, 'manifest')
    if not os.path.isfile(manifest_path):
        raise Exception("File does not exist (or not a file): %s" % manifest_path)
    manifest = {}
    execfile(manifest_path, {}, manifest)
    return dict(name = os.path.basename(themedir), label = manifest['name'])

themes = [themedict(path) for path in themedirs]
theme_map = dict((theme['name'], theme) for theme in themes)
theme_codes = themedirs
languages = [dict(label=label, name=code) for label, code in [ ('English', 'en'), ('German', 'de') ]]
lang_map = dict((lang['name'], lang) for lang in languages)
lang_codes = tuple(lang_map.keys())

class BuilderBase(object):
    def __init__(self, page, path):
        self.page = page
        self.path = path
    def gen_path_combinations(self):
        build_data = dict(theme=theme_codes, lang=lang_codes)
        pathvars = [var[2:-2] for var in self.path.split(os.path.sep) if var.startswith('%')]
        combinations = itertools.product(*([{var: v} for v in build_data[var]] for var in pathvars))
        return combinations

    def build(self):
        """
        To be implemented by concrete class
        """

class PageBuilder(BuilderBase):
    def build(self):
        for path_data in self.gen_path_combinations():
            d = {}
            for elem in path_data:
                d.update(elem)
            path = pathjoin(pubroot, (self.path % d))
            print("Building page: %s" % path)
            page = self.page()
            page_data = d
            page_data['rroot'] = os.path.sep.join('..' for p in self.path.split(os.path.sep))
            page.write(path, page_data)

class JSBuilder(BuilderBase):
    """
    """

prefix = '%(lang)s/%(theme)s/'

pages = [PageBuilder(pagelib.InvoicingPage, prefix + 'invoicing/home'),
         PageBuilder(memberlib.MemberCreate, prefix + 'member/new'),
         PageBuilder(pagelib.LoginPage, 'login'),
         PageBuilder(bizplacelib.BizplaceCreate, prefix + 'bizplace/create'),
         PageBuilder(planlib.PlanCreate, prefix + 'plan/create'),
         PageBuilder(resourcelib.ResourceCreate, prefix + 'resource/create'),
         PageBuilder(pagelib.SuperuserCreate, 'setup'),
         PageBuilder(pagelib.Dashboard, prefix + 'dashboard'),
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

def build_themes():
    """
    theme dir (built) goes to <pub>/themes/<theme-name>
    """
    base_themedir = pathjoin(themeroot, 'base')
    for themedir in themedirs:
        src_themedir = pathjoin(themeroot, themedir)
        dst_themedir = pathjoin(pubroot, 'themes', themedir)
        # 1. copy images
        base_imagedir = pathjoin(base_themedir, 'images')
        src_imagedir = pathjoin(src_themedir, 'images')
        dst_imagedir = pathjoin(dst_themedir, 'images')
        copydirs(base_imagedir, dst_imagedir)
        if os.path.exists(src_imagedir) and os.listdir(src_imagedir):
            copydirs(src_imagedir + '/*', dst_imagedir)
        # 2. compile style
        infile = pathjoin(src_themedir, 'css', 'main.scss')
        outfile = pathjoin(dst_themedir, 'css', 'main.css')
        styledir = os.path.dirname(outfile)
        open(infile, 'w').write(open(pathjoin(base_themedir, 'css', 'main.scss')).read())
        if not os.path.exists(styledir):
            os.makedirs(styledir)
        cmd = scsscompile_cmd % dict(infile=infile, outfile=outfile)
        os.system(cmd)
        os.remove(infile)

def build_scripts():
    """
    source scripts would need to know context (lang, theme, role) hence goes to go to /<theme>/<lang>/<role>/<path>
    """
    scripts = pathjoin(srcroot, 'js', '*')
    copydirs(scripts, pathjoin(pubroot, 'js'))

def build_all():
    for page in pages:
        page.build()


def main():
    if not os.path.exists(pubroot):
        os.makedirs(pubroot)
    copy_contribs()
    build_themes()
    build_scripts()
    build_all()

if __name__ == '__main__':
    main()
