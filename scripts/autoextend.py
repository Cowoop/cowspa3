import os
import sys
rootdir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, rootdir)
import be.bootstrap
be.bootstrap.start()
import be.apis.membership as membershiplib
import be.apis.user as userlib

userlib.set_context(env.config.system_username, 0)
membershiplib.autoextend()
env.context.pgcursor.connection.commit()
