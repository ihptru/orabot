#!/bin/python
from BeautifulSoup import BeautifulSoup
import urllib

url = 'http://openra.res0l.net/download/linux/deb/index.php'
stream = urllib.urlopen(url).read()
soup = BeautifulSoup(stream)
words = soup.prettify()
release = words.split('<ul')[1].split('<li')[1].split()[3]
playtest = words.split('<ul')[2].split('<li')[1].split()[3]
filename = 'version'
file = open(filename, 'w')
file.write(release + " " + playtest)
file.close()
