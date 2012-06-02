# Suggested cron job 
MAILTO=address@example.com

# Changing to source directory helps supervisord to find
# - conf in current directory
# - various paths defined in conf eg. path to store logs/pids
#
# Invoking supervisord starts supervisord in daemon mode if it hasn't already started and also starts all programs configured to autostart 

*/30 * * * * /home/<username>/<apphome>/<source> && ../bin/supervisord
