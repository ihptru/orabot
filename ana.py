#!/bin/python
import pyanagrams
import random
import sys

word = " ".join(sys.argv[1:])
anagrams = pyanagrams.getanagrams(word)
w_choice = random.choice(anagrams)
filename = 'anagram.txt'
file = open(filename, 'w')
file.write(w_choice)
file.close()
