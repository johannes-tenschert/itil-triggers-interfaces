#!/usr/bin/env python
import re
from sys import stdin

p = re.compile('^([a-zA-Z_]+)\s*->\s*([a-zA-Z_]+)\s*(\[.*\])?\s*;$')
empty = re.compile('^\s*$')
start_copy = re.compile('^// COPY ALL$')
end_copy = re.compile('^// END COPY ALL$')

blindly_copy = False
copy = list()
unidirectional = list()
bidirectional = list()

for line in stdin.readlines():
	if start_copy.match(line):
		blindly_copy = True
	elif end_copy.match(line):
		blindly_copy = False

	if not blindly_copy:
		res = p.match(line)
		if res == None and empty.match(line) == None:
			pass
		if res != None:
			a = res.group(1)
			b = res.group(2)
			if (b, a) in unidirectional:
				unidirectional.remove((b, a))
				bidirectional.append((b, a))
			else:
				unidirectional.append((a, b))
	else:
		copy.append(line)

print "digraph G {"
print "overlap=false;"
print "splines=true;"

for line in copy:
	print line[0:-1]

for (a, b) in unidirectional:
	print "%s -> %s [color=black];" % (a, b)

for (a, b) in bidirectional:
	print "%s -> %s [dir=both;color=black;];" % (a, b)

print "//INFO: unidirectional: %d, bidirectionalt: %d" % (len(unidirectional), len(bidirectional))
print "}"
