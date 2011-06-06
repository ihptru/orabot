#!/usr/bin/env python
"""Command Line Options:
-h --help : Prints the instruction on how to use this module

Exposed Methods:
    getanagrams(word)
    getGIF(sourceString,
           targetString,
           [textColor,]
           [backgroundColor,]
           [border_color,]
           [delay,]
           )
    getmoreanagrams(anagram,
                    [language,]
                    [t,]
                    [d,]
                    [include,]
                    [exclude,]
                    [n,]
                    [m,]
                    [a,]
                    [l,]
                    [q,]
                    [k,]
                    )

For Usage and Docs:
    >>> import pyanagrams
    >>> pyanagrams.getanagrams.__doc__
    >>> pyanagrams.getGIF.__doc__
    >>> pyanagrams.getmoreanagrams.__doc__

"Copyright (c) 2010 Shiv Deepak"

Disclaimer:
The author of this module kept the code as bug free as possible,
but the Anagram Server is located a 'http://wordsmith.org/anagram/', 
The author should not be held responsible for the reliability of data
from the anagram server or what so ever.
Users should use this code on their own risk.
"""

__author__ = "Shiv Deepak (idlecool@gmail.com)"
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2010/11/29 22:19:59 $"
__copyright__ = "Copyright (c) 2010 Shiv Deepak"
__license__ = "GPL"

import urllib
import sys
import getopt

from BeautifulSoup import BeautifulSoup

servicedomain = 'http://wordsmith.org'
webservice = 'http://wordsmith.org/anagram/'

def getanagrams(word):
    """Gets anagrams for given word,
return value will be a list,
how to call: getanagram(str(word))
"""
    urlprefix = 'anagram.cgi?anagram='
    urlsuffix = '&t=1000&a=n'
    processurl = webservice+urlprefix+word+urlsuffix
    stream = urllib.urlopen(processurl).read()
    soup = BeautifulSoup(stream)
    body = soup.contents[2]
    block = body.contents[3]
    list = block.contents[5]
    words = list.contents[7]
    wordstring = words.prettify()
    wordlist = wordstring.split('\n<br />\n')[1:-1]
    return wordlist


def getGIF(sourceString,\
               targetString,\
               textColor='#00FFFF',\
               backgroundColor='#FF0000',\
               border_color='#000000',\
               delay='slow',\
               ):
    """Gets the GIF animation for provided anagram,
return value will be a binary stream,
how to call: getGIF(sourceString,
                    targetString,
                    [textColor,]
                    [backgroundColor,]
                    [border_color,]
                    [delay,]
                    )
all colour should be RGB Hex coded ex: #FF09E7 
and delay has three options ['fast','medium','slow']
"""
    #Anagram check for source and target strings.
    sourceString = sourceString.lower()
    targetString = targetString.lower()
    sName = list(sourceString)
    tName = list(targetString)
    for i in xrange(sName.count(' ')):
        sName.remove(' ')
    for i in xrange(tName.count(' ')):
        tName.remove(' ')
    if(len(sName) != len(tName)):
        raise AnagramException(sourceString, targetString)
    for char in sName:
        try:
            tName.remove(char)
        except Exception:
            raise AnagramException(sName, tName)
    
    #Prepare url to generate gif.
    gifcgi = 'animation.cgi?'
    processurl = webservice +\
        gifcgi +\
        urllib.urlencode({'sourceString':sourceString,\
                              'submit':'Generate Animated Gif',\
                              'targetString':targetString,\
                              'textColor':textColor,\
                              'backgroundColor':backgroundColor,\
                              'border_color':border_color,\
                              'delay':delay,\
                              })
    stream = urllib.urlopen(processurl).read()
    soup = BeautifulSoup(stream)
    body = soup.contents[2]
    cont = body.contents[3]
    cont2 = cont.contents[5]
    cont3 = cont2.contents[7]
    imgelement = str(cont3.extract())
    urlpath = imgelement.split('"')[1]
    imgurl = servicedomain + urlpath
    
    #Fetch the gif image.
    stream = urllib.urlopen(imgurl).read()
    return stream


def getmoreanagrams(anagram,\
                        language='english',\
                        t='1000',\
                        d='',\
                        include='',\
                        exclude='',\
                        n='',\
                        m='',\
                        a='n',\
                        l='n',\
                        q='n',\
                        k='1',\
                        ):
    """SYNTAX:
    
         getmoreanagrams(anagram,
                         [language,]
                         [t,]
                         [d,]
                         [include,]
                         [exclude,]
                         [n,]
                         [m,]
                         [a,]
                         [l,]
                         [q,]
                         [k,]
                         )

         return value will be a list
    
OPTIONS:

      i) anagram: Word/phrase to be anagrammed: any value except ""

     ii) language: Generate anagrams in this language:
         english           : English
         english-obscure   : English (with obscure words) 
         german            : Deutsch (German) 
         spanish           : Espa&ntilde;ol (Spanish) 
         french            : Fran&ccedil;ais (French)
         italian           : Italiano (Italian)
         latin             : Latin
         dutch             : Nederlands (Dutch)
         portuguese        : Portugu&ecirc;s (Portuguese)
         swedish           : Svenska (Swedish)
         names             : Names (proper names only)
    iii) t : Display maximum this many anagrams:
         0    : for no limit
         1000 : should be default

     iv) d : Maximum number of words in each anagram:
   
      v) include : Anagrams must include this word:

     vi) exclude : Anagrams must exclude these words:

    vii) n : Minimum number of letters in each word:

   viii) m : Maximum number of letters in each word:

     ix) a : Repeat occurrences of a word OK:
         True  : y
         False : n

      x) l : Show candidate word list only:
         True  : y
         False : n

     xi) q : Show line numbers with anagrams:
         True  : y
         Flase : n

    xii) k : Show anagrams in lower or uppercase:
         lower       : 0
         First Upper : 1
         UPPER       : 2

    """
    submit = 'Find Anagrams'
    source = 'adv'
    if len(anagram) == 0:
        raise AdvAnagramExcept('Anagram String Is Empty!!!')
    if language not in ['english',\
                            'english-obscure',\
                            'german',\
                            'spanish',\
                            'french',\
                            'italian',\
                            'latin',\
                            'dutch',\
                            'portuguese',\
                            'swedish',\
                            'names',\
                            ]:
        raise AdvAnagramExcept('Language not supported')
    if a not in ['y','n']:
        raise AdvAnagramExcept("value of 'Repeat occurrences of a word OK' should be either 'y' or 'n'")
    if l not in ['y','n']:
        raise AdvAnagramExcept("value of 'Show candidate word list only' should be either 'y' or 'n'")
    if q not in ['y','n']:
        raise AdvAnagramExcept("value of 'Show line numbers with anagrams' should be either 'y' or 'n'")
    if k not in ['0','1','2']:
        raise AdvAnagramExcept('value of a should be either str(0) or str(1) or str(2)')
    urlprefix = 'anagram.cgi?'
    processurl = webservice +\
        urlprefix +\
        urllib.urlencode({ 'anagram' : anagram,\
                               'submit': submit,\
                               'language': language,\
                               't':t,\
                               'd':d,\
                               'include':include,\
                               'exclude':exclude,\
                               'n':n,\
                               'm':m,\
                               'a':a,\
                               'l':l,\
                               'q':q,\
                               'k':k,\
                               })
    stream = urllib.urlopen(processurl).read()
    soup = BeautifulSoup(stream)
    body = soup.contents[2]
    block = body.contents[3]
    list = block.contents[5]
    words = list.contents[7]
    wordstring = words.prettify()
    wordlist = wordstring.split('\n<br />\n')[1:-1]
    return wordlist
    

class AnagramException(Exception):
    def __init__(self, sName, tName):
        self.sName = sName
        self.tName = tName
    def __str__(self):
        return "'" +\
            self.sName +\
            "' & '" +\
            self.tName +\
            "' are not anagrams!!!"


class AdvAnagramExcept(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


def _usage():
    """Prints instructions on how to use this module """
    #print __doc__

if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError:
        _usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            _usage()
            sys.exit()
    if args:
        anagram = " ".join(args)
    else:
        anagram = "Anagrams"
    anagramlist = getanagrams(anagram)
    print "Word:"
    print "    "+anagram
    print
    print "Anagrams:"
    if anagramlist:
        for eachanagram in anagramlist:
            print '    ' + eachanagram
    else:
        print '    No Anagrams Possible'
    print
