import os
import sys
import datetime
import subprocess

# Below path manipulation is done so that script could run independently from outside virtual env
# however packaging should provide a better option
config_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, config_dir)

import commonlib.readconf

app_name = "cowoop_prod"
start_time = datetime.datetime.now()
backup_dir = os.path.join(os.environ['HOME'], 'backups')
backup_file = app_name + '-' + start_time.isoformat()
backup_path = os.path.join(backup_dir, backup_file)
pgpass_file = ".pass-" + app_name
pgpass_path = os.path.join(backup_dir, pgpass_file)

pg_backup_cmd = ["pg_dump", "-Fc" % dict(backup_path=backup_path)]

def prep():
    config = commonlib.readconf.parse_config()
    pgconf = dict(database='', user='', host='', port='', password='')
    pgconf.update(config.pgdb)
    # http://www.postgresql.org/docs/9.1/static/libpq-pgpass.html
    pgpass_content = "%(host)s:%(port)s:%(database)s:%(user)s:%(password)s" % pgconf
    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)
    pgpass_fd = open(pgpass_path, 'w')
    pgpass_fd.write(pgpass_content)
    pgpass_fd.close()
    os.chmod(pgpass_path, 0600)
    os.environ['PGPASSFILE'] = pgpass_path

def cleanup():
    os.remove(pgpass_path)

def pg_backup():
    p = subprocess.Popen(pg_backup_cmd, stderr=subprocess.PIPE, stdout=open(backup_path, 'w'))
    stdout, stderr = p.communicate()
    end_time = datetime.datetime.now()
    delta = end_time - start_time
    if p.returncode != 0:
        sys.stderr.write('Postgres backup failed\n')
        sys.stderr.write(str(stderr))
    return p.returncode

def main():
    prep()
    retcode = pg_backup()
    cleanup()
    sys.exit(retcode)

main()
