####################
#####  IRC Bot Config  #####
####################

server1 = {
            # server to connect
            'host' : 'irc.freenode.net',

            # server port
            'port' : 6667,

            # channels to connect to (space as delimiter)
            'channels' : '#change_channel1 #change_channel2',

            # bot nick
            'bot_nick' : 'change_bot_nick',

            # identify with NickServ? ( True or False )
            'nickserv' : False,

            # nickserv password
            'nickserv_password' : '',

            # commands start with:
            'command_prefix' : ']',

            # global timeout (how long command is executing)
            'command_timeout' : 20,

            # write channel logs?
            'write_logs' : False,

            # channel to write logs of (space as delimiter)
            'log_channels' : '#change_channel1 #change_channel2',

            # support plugins? ( True or False )
            'plugins_support' : False,

            # write bug reports to (space as delimiter)
            'write_bug_notifications_to' : '',

            # write new commit notifications to (space as delimiter)
            'write_commit_notifications_to' : '',

            # GitHub repositories from where fetch new commit data (space as delimiter); Ex: https://github.com/OpenRA/OpenRA
            'git_repos' : '',

            # Change topic of next channel in notifications process (space as delimiter):
            'change_topic_channel' : '',
}

### To add more server connections, simply create a new dictionary similar to previous one (`server1`) and do not forget to add it's name to a list below (`servers`) ###

servers = ['server1']

# Next configs are global for all bot instances

#log directory
log_dir = 'logs/'

# commands related:
randomserver_dir = ''   # directory where files of (randomserver) command are saved (with / at the end)
randomserver_url = ''   # url path to that directory    (with / at the end)

randomteam_dir = '' #directory where files of (randomteam) command are saved (with / at the end
randomteam_url = '' #url path to that directory (with / at the end)

# Stream Server
stream_server_address = ""
stream_server_port = 0

# Path to OpenRA game (pickup system)
openra_path = ""
