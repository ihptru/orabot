###################
### Server Data ###
###################

#server to connect
server = 'irc.freenode.net'

#server port
port = 6667

#channels to connect to (comma as delimiter)
channels = '#channel1,#channel2'

#write channel logs?
write_logs = False

#log directory
log_dir = '../logs/'

#channel to write logs of (comma as delimiter)
log_channels = '#channel1,#channel2'



################
### Bot Data ###
################

#bot nick
bot_nick = 'change_bot_nick'

#identify with NickServ? ( True or False )
nickserv = False

#nickserv password
nickserv_password = ''


#commands start with:
command_prefix = ']'


#####################
### Notifications ###
#####################

#support notifications? ( True or False )
notifications = False

### write bug reports to (comma as delimiter)
write_bug_notifications_to = '#openra'

### write new commit notifications to (comma as delimiter)
write_commit_notifications_to = '#openra-dev'

### GitHub repositories from where fetch new commit data (space as delimiter); Ex: https://github.com/OpenRA/OpenRA
git_repos = 'https://github.com/chrisforbes/OpenRA https://github.com/hamb/OpenRA'
