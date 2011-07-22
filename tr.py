#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from translate import Translator

translate = Translator().translate
languages=['af','sq','ar','be','bg','ca','zh-CN','hr','cs','da','nl','en','et','tl','fi','fr','gl','de','el','iw','hi','hu','is','id','ga','it','ja','ko','lv','lt','mk','ml','mt','no','fa','pl','ro','ru','sr','sk','sl','es','sw','sv','th','tr','uk','vi','cy','yi']

filename = 'tr.temp'
file = open(filename, 'r')
text = file.readline()
file.close()

lst = text.split(' ')
t_from = lst[1]
t_to = lst[2]
if t_from in languages:
    if t_to in languages:
        junk = lst.pop(0)
        junk = lst.pop(0)
        junk = lst.pop(0)
        
        length = len(lst)   # must be only text left
        line = ''
        for i in range(length):
            line = line+' '+lst[i]+' '
        line=line.lstrip().rstrip()
 
        text_to_file = translate(line, lang_to=t_to, lang_from=t_from)

        filename = 'tr.text'
        file = open(filename, 'w')
        file.write(text_to_file)
        file.close()
