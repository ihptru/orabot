#####  IRC Bot Config  #####
server1 = {
            # server to connect
            'host' : 'irc.freenode.net',

            # server port
            'port' : 6667,

            # channels to connect to (space as delimiter)
            'channels' : '#change_channel1 #change_channel2',

            # bot nick
            'bot_nick' : 'change_bot_nickname',

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

            # channels to write logs of (space as delimiter)
            'log_channels' : '#change_channel1 #change_channel2',

            # support tools? ( True or False )
            'tools_support' : False,

            # write bug reports to next channels (space as delimiter), if plugins_support is True
            'write_bug_notifications_to' : '',

            # write new commit notifications to next channels (space as delimiter), if plugins_support is True
            'write_commit_notifications_to' : '',

            # GitHub repositories from where we will fetch NEW commit info (space as delimiter); Ex: https://github.com/OpenRA/OpenRA
            'git_repos' : '',
}

# To add more server connections, simply create a new dictionary similar to previous one (`server1`)
# and do not forget to add it's name to a list below (servers); Ex: server = ['server1','server2']

servers = ['server1']

# Next configs are global for all bot instances

#log directory
log_dir = 'logs/'
