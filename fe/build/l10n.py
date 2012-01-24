from run import exec_cmd

def extract_msgs():
    cmd = "pybabel extract --no-location --omit-header -F fe/build/mapping.ini -o cowspa.pot fe/src/"
    exec_cmd(cmd)
    #TODO : If locale specific .po file exists, merge the message catalog
    for lang in ['en','de']:
        cmd = "pybabel init -D cowspa --locale=" + lang + " -i cowspa.pot -d l10n"
        exec_cmd(cmd)

if __name__ == '__main__':
    extract_msgs()
