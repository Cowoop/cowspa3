from run import exec_cmd

def extract_msgs():
    cmd = "/usr/bin/pygettext -d cowspa --no-location -o cowspa.pot fe/src/*.py"
    exec_cmd(cmd)
    for lang in ['en','de']:
        cmd = "msginit --no-translator --locale=" + lang + " --input=cowspa.pot -o l10n/" + lang + "/" + lang + ".po"
        exec_cmd(cmd)

if __name__ == '__main__':
    extract_msgs()
