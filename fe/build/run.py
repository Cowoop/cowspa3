import os
import sys
import itertools
import glob

sys.path.append('.')

import sphc
import commonlib.helpers
commonlib.helpers.setdefaultencoding()

import fe
import fe.src.pages
import fe.src.pages as pagelib
import fe.src.pages.invoicing
import fe.src.member_pages as memberlib
import fe.src.bizplace_pages as bizplacelib
import fe.src.plan_pages as planlib
import fe.src.resource_pages as resourcelib
import commonlib.shared.static as static

option_no_themes = '--nothemes' in sys.argv

pathjoin = os.path.join

pubroot = 'pub'
buildroot = 'build'
contribroot = 'fe/contrib'
srcroot = 'fe/src'
contribs = ['js', 'css', 'images']
roles = ['host']
themeroot = static.themeroot
themedirs = [os.path.basename(name) for name in glob.glob(themeroot + '/*') if os.path.isdir(name)]
themedirs.remove('base')
compass_bin = "/var/lib/gems/1.8/gems/compass-0.11.5/bin/compass"

def exec_cmd(cmd, fail_on_err=True):
    print("Executing :" + cmd)
    ret = os.system(cmd)
    if fail_on_err and not ret == 0:
        sys.exit("Command failed: %s" % cmd)
    return ret

def compile_scss(prjdir):
    opts = "-q -r susy -u susy --relative-assets --sass-dir scss --css-dir css" % locals()
    project_cmd = compass_bin + " create %(prjdir)s %(opts)s" % locals()
    exec_cmd(project_cmd)
    compile_cmd = compass_bin + " compile %(prjdir)s -e production --force " % locals()
    exec_cmd(compile_cmd)

themes = static.themes
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
         PageBuilder(pagelib.Login, 'login'),
         PageBuilder(pagelib.Activation, 'activate'),
         PageBuilder(bizplacelib.BizplaceCreate, prefix + 'bizplace/new'),
         PageBuilder(planlib.PlanCreate, prefix + 'bizplace/tariffs'),
         PageBuilder(resourcelib.ResourceCreate, prefix + 'resource/new'),
         PageBuilder(pagelib.Dashboard, prefix + 'dashboard'),
         PageBuilder(memberlib.MemberProfile, prefix + 'profile'),
         PageBuilder(fe.src.pages.invoicing.New, prefix + 'invoicing/new'),
         PageBuilder(pagelib.LogoutPage, 'logout'),
         PageBuilder(fe.src.pages.invoicing.Preferences, prefix + 'invoicing/preferences'),
         PageBuilder(fe.src.pages.invoicing.History, prefix + 'invoicing/history')
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
    copydirs(themeroot, pubroot)
    base_themedir = pathjoin(themeroot, 'base')
    for themedir in themedirs:
        # cp -r fe/src/themes pub
        # cp -r contrib/css/* pub/themes/default/scss/
        # cp -r themes/base/scss pub/themes/default/scss/base
        # cp pub/themes/default/scss/base/main.scss pub/themes/default/scss/
        # compass create . --sass-dir themes/default/scss --css-dir themes/default/css
        # rm pub/themes/default/scss
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
        src_scssdir = pathjoin(src_themedir, 'css')
        dst_scssdir = pathjoin(dst_themedir, 'scss')
        dst_cssdir = pathjoin(dst_themedir, 'css')
        copydirs(themeroot, pubroot)
        copydirs(pathjoin(contribroot, 'css'), pathjoin(dst_scssdir, 'contrib'))
        copydirs(pathjoin(base_themedir, 'scss'), pathjoin(dst_scssdir, 'base'))
        copydirs(pathjoin(dst_scssdir, 'base', 'main.scss'), dst_scssdir)
        compile_scss(dst_themedir)
        # 3. copy jquery-ui images
        src_jqui_imagedir = pathjoin(contribroot, 'js', 'jquery-ui', 'images')
        copydirs(src_jqui_imagedir, dst_cssdir)

def build_scripts():
    """
    source scripts would need to know context (lang, theme, role) hence goes to go to /<theme>/<lang>/<role>/<path>
    """
    scripts = pathjoin(srcroot, 'js', '*')
    copydirs(scripts, pathjoin(pubroot, 'js'))

def build_be_template_styles():
    base_dir = 'be/templates'
    compile_scss(base_dir)

def build_all():
    for page in pages:
        page.build()

def main():
    if not os.path.exists(pubroot):
        os.makedirs(pubroot)
    copy_contribs()
    build_be_template_styles()
    if not option_no_themes: build_themes()
    build_scripts()
    build_all()

if __name__ == '__main__':
    main()
