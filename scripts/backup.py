import os
import sys
import datetime
import subprocess

# Below path manipulation is done so that script could run independently from outside virtual env
# however packaging should provide a better option
config_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, config_dir)

import commonlib.readconf

config = commonlib.readconf.parse_config()

app_name = config.name
start_time = datetime.datetime.now()
backup_dir = os.path.join(os.environ['HOME'], 'backups')
backup_file = app_name + '-' + start_time.isoformat()
backup_path = os.path.join(backup_dir, backup_file)
pgpass_file = ".pass-" + app_name
pgpass_path = os.path.join(backup_dir, pgpass_file)

pg_backup_cmd = ["pg_dump", "-Fc" % dict(backup_path=backup_path)]

def pg_prep():
    pgconf = dict(database='*', user='*', host='*', port='*', password='')
    pgconf.update(config.pgdb)
    # http://www.postgresql.org/docs/9.1/static/libpq-pgpass.html
    pgpass_content = "%(host)s:%(port)s:%(database)s:%(user)s:%(password)s" % pgconf
    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)
    pgpass_fd = open(pgpass_path, 'w')
    pgpass_fd.write(pgpass_content)
    pgpass_fd.close()
    os.chmod(pgpass_path, 0600)
    env = dict(os.environ)
    env['PGUSER'] = pgconf['user']
    env['PGDATABASE'] = pgconf['database']
    env['PGPASSFILE'] = pgpass_path
    return env

def cleanup():
    os.remove(pgpass_path)

def pg_backup():
    env = pg_prep()
    p = subprocess.Popen(pg_backup_cmd, stderr=subprocess.PIPE, stdout=open(backup_path, 'w'), env=env)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        sys.stderr.write('Postgres backup failed\n')
        sys.stderr.write(str(stderr))
    else:
        end_time = datetime.datetime.now()
        sys.stdout.write("PG Backup is successful\n")
        sys.stdout.write("App name: %s\n" % config.name)
        sys.stdout.write("Database: %s\n" % config.pgdb['database'])
        sys.stdout.write("It took %s complete.\n" % (end_time - start_time))
    return p.returncode

def main():
    retcode = pg_backup()
    cleanup()
    sys.exit(retcode)

main()
