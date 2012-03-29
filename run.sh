#! /bin/bash -e

# activate the app's virtual environment.
bash ../bin/activate

# export LD_LIBRARY_PATH, because a process can not change the env of its 
# parent process, so have to do it here instead of in supervisord.conf

export LD_LIBRARY_PATH=`pwd`/lib:$LD_LIBRARY_PATH

# start the supervisor daemon

supervisord -c supervisord.conf

