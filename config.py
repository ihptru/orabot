#####  IRC Bot Config  #####
server1 = {
            # server to connect
            'host' : 'irc.freenode.net',

            # server port
            'port' : 6667,

            # channels to connect to (space as delimiter)
            'channels' : '#openra #openra-dev',

            # bot nick
            'bot_nick' : 'orabot',

            # identify with NickServ? ( True or False )
            'nickserv' : False,

            # nickserv password
            'nickserv_password' : '',

            # commands start with:
            'command_prefix' : ']',

            # global timeout (how long command is executing)
            'command_timeout' : 20,

            # write channel logs?
            'write_logs' : True,

            # channels to write logs of (space as delimiter)
            'log_channels' : '#openra',

            # support tools? ( True or False )
            'tools_support' : True,
            
            # log directory
            'log_dir' : 'logs/',

            # specify commands which this instance must not support (space as delimiter)
            'do_not_support_commands' : '',

            # support spam_filter on specific network?
            'spam_filter_support': True,

            # authenticate over `oper` to OP itself?
            'use_oper': True,

            # `oper` password
            'oper_password': '',

            # OP itself over `oper` on channels (space as delimiter):
            'oper_channels': ''
}

# To add more server connections, simply create a new dictionary similar to previous one (`server1`)
# and do not forget to add it's name to a list below (servers); Ex: server = ['server1','server2']

servers = ['server1']
