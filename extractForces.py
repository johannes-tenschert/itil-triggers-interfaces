#!/usr/bin/env python

from config import *
import sys

books = []
for f in filenames:
	books.append(getBook(f))

setalias = True

points = ["assertive", "commissive", "declarative", "directive", "expressive"]
pointalias = dict()
for i in range (0, len(points)):
	pointalias[points[i]] = str(i + 1)

outputfinished = []

for b in books:
	sys.stdout.write("\\section{%s}\n" % b.name)
	
	# Boilerplate BEGIN longtable
	sys.stdout.write("\\begin{longtable}{|p{.6\linewidth}|p{.4\linewidth}|}\n")
	sys.stdout.write("\t\\hline\n")
	sys.stdout.write("\tTrigger & Illocutionary Force$_\\text{Illocutionary Point(s)}$ \\\\\n")
	sys.stdout.write("\t\\hline\n")
	sys.stdout.write("\t\\endhead\n\n")
	
	def checkTrigger(process, trigger):
		for content in trigger.content:
			if isinstance(content, SAClass) and content.classification == "speechact":
				def formatForce(force):
					global points
					currentpoints = []
					for p in points:
						if force.__dict__[p]:
							currentpoints.append(p)
					if setalias:
						return "%s$_{%s}$" % (force.name, "".join(map(lambda x: pointalias[x], currentpoints)))
					else:
						return "%s$_{%s}$" % (force.name, ",".join(currentpoints))
				forces = ", ".join(map(formatForce, content.forces))
				
				# Output process
				if not process in outputfinished:
					sys.stdout.write("\t\\hline \\multicolumn{2}{|l|}{\\textbf{")
					sys.stdout.write(process.name)
					sys.stdout.write("}} \\\\\n")
					outputfinished.insert(0, process)
				
				sys.stdout.write("\t\\hline %s & %s \\\\\n" % (content.latexContent(), forces))

			elif isinstance(content, Trigger):
				checkTrigger(process, content)
	
	for process in b.processes:
		for trigger in process.triggers:
			checkTrigger(process, trigger)
	
	sys.stdout.write("\t\\hline\n\n")
	# Boilerplate END longtable
	sys.stdout.write("\\end{longtable}\n")
