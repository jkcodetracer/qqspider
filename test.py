#!/usr/bin/python

import re

dic = {}
lis = []
spliter = re.compile('\\W*')
for line in file('init_messages.py'):
	lowline = [s.lower() for s in spliter.split(line)]
	for word in lowline:
		dic.setdefault(word, 0)
		dic[word] += 1

for key,value in dic.items():
	lis.append((value, key))

lis.sort()
lis.reverse()

for (key,value) in lis:
	print key,' ',value

