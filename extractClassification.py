#!/usr/bin/env python

from config import *

books = []
for f in filenames:
	books.append(getBook(f))

if printBookStatistics:
	printStatistics(books)

for b in books:
	b.latex()
