#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys

# Options

filenames = ["raw/ServiceStrategy.xml", "raw/ServiceDesign.xml", "raw/ServiceTransition.xml", "raw/ServiceOperation.xml", "raw/ContinualServiceImprovement.xml"]
afterProcess = "" # "\\clearpage\n"
printProcessStatistics = True
printBookStatistics = True

# LaTeX formatting

def latex(output):
	if (output == None):
		return ""
	return output # Escaping goes here... (as soon as necessary!)

latexbook = "section"
latexprocess = "subsection"
itemize = "enumerate"

types = ["speechact", "decision", "artifact", "periodic", "observation", "system event"]
colors = {"speechact" : ("red", "white"), \
          "periodic" : ("yellow", "black"), \
          "decision" : ("cyan", "white"), \
		  "artifact" : ("lime", "black"), \
		  "observation" : ("brown", "white"), \
		  "system event" : ("magenta", "white"), \
          "none" : ("black", "white")} # Just highlight

# Data structures

def printStatistics(raw):
	counter = dict()
	for key in types:
		counter[key] = 0
	
	sys.stdout.write("\\noindent{\\small\\begin{tabular}{|p{3cm}%s|c|}\n" % ("|c" * len(types)))
	sys.stdout.write("\\hline & ")
	for key in types:
		sys.stdout.write("{\\scriptsize %s} & " % latex(key))
	sys.stdout.write("$\\Sigma$ \\\\\n")
	
	for i in raw:
		sys.stdout.write("\\hline {\\scriptsize %s} & " % latex(i.name))
		cnt = 0
		for key in types:
			res = i.countType(key)
			cnt += res
			counter[key] += res
			sys.stdout.write("%s & " % (str(res) if res > 0 else ""))
		sys.stdout.write("%s \\\\\n" % str(cnt))
	
	sys.stdout.write("\\hline $\\Sigma$ & ")
	cnt = 0
	for key in types:
		cnt += counter[key]
		sys.stdout.write("%s & " % str(counter[key]))
	sys.stdout.write("%s \\\\\n" % str(cnt))
	sys.stdout.write("\\hline\n\\end{tabular}}\n")

class Book:
	"""Container for all processes and triggers of a book"""
	
	def __init__(self, name):
		self.processes = []
		self.name = name

	def addProcess(self, process):
		if isinstance(process, Process):
			self.processes.append(process)

	def getProcesses(self):
		return self.processes

	def text(self, begin = "", sep = "   "):
		print begin + "Book: " + str(self.name)
		for p in self.processes:
			p.text(begin + sep, sep)
		print
	
	def latex(self):
		sys.stdout.write("\\%s{%s}\n" % (latexbook, latex(self.name)))
		
		first = True
		
		if printProcessStatistics:
			printStatistics(self.processes)
					
		for p in self.processes:
			if first:
				first = False
			else:
				sys.stdout.write(afterProcess)
			p.latex()

	def countType(self, _type):
		res = 0
		for p in self.processes:
			res += p.countType(_type)
		return res


class Process:
	"""Container for all triggers of a process"""
	
	def __init__(self, name):
		self.triggers = []
		self.name = name

	def addTrigger(self, trigger):
		self.triggers.append(trigger)

	def text(self, begin, sep):
		print begin + "Process: " + str(self.name)
		for t in self.triggers:
			t.text(begin + sep, sep)

	def latex(self):
		sys.stdout.write("\\%s{%s}" % (latexprocess, latex(self.name)))
		sys.stdout.write("\\begin{%s}" % itemize)
		for t in self.triggers:
			sys.stdout.write("\\item ")
			t.latex()
			sys.stdout.write("\n")
		sys.stdout.write("\\end{%s}\n" % itemize)

	def countType(self, _type):
		res = 0
		for t in self.triggers:
			res += t.countType(_type)
		return res


class TriggerContent:
	pass


def alignText(output, begin, first = "", after = ""):
	lines = output.splitlines()
	for l in lines:
		print begin + first + l
		first = after

class SAClass(TriggerContent):
	"""Container for classification"""
	
	def __init__(self, classification):
		self.content = []
		self.classification = classification
		self.forces = []
	
	def addText(self, content):
		if content != None:
			self.content.append(TextContent(content))
	
	def addLaTeX(self, content):
		if content != None:
			self.content.append(LaTeXContent(content))

	def addForce(self, force):
		self.forces.append(force)

	def text(self, begin, sep):
		content = ""
		for o in self.content:
			if isinstance(o, TextContent):
				content += o.text
			elif isinstance(o, LaTeXContent):
				content += o.tex
		print begin + "Class(" + str(self.classification) + "):"
		alignText("[" + content + "]", begin + sep)
	
	def latexContent(self):
		content = ""
		for o in self.content:
			if isinstance(o, TextContent):
				content += latex(o.text)
			elif isinstance(o, LaTeXContent):
				content += o.tex
		return content
	
	def latex(self):
		content = self.latexContent()
		clr = colors[self.classification]
		sys.stdout.write("\\hlc{%s}{%s}{%s$_{\\mbox{\\tiny %s}}$}" % (clr[0], clr[1], content, self.classification))

class Force:
	"""Container for illocutionary force"""
	
	def __init__(self, name):
		self.name = name
		self.assertive = False
		self.commissive = False
		self.declarative = False
		self.directive = False
		self.expressive = False

class Trigger(TriggerContent):
	"""Container for all contents of a trigger"""
	
	def __init__(self):
		self.content = []

	def addContent(self, content):
		self.content.append(content)
	
	def addText(self, content):
		if content != None:
			self.content.append(TextContent(content))

	def text(self, begin, sep):
		current = ""
		realfirst = "- "
		first = realfirst
		after = "  "

		for o in self.content:
			if isinstance(o, TextContent):
				current += o.text
			elif isinstance(o, LaTeXContent):
				current += o.tex
			else:
				# Output current
				if current != "":
					alignText(current, begin, first, after)
					first = after
					current = ""
				
				if first == realfirst:
					print begin + first + "Trigger:"
					first = after
				
				if isinstance(o, Trigger):
					o.text(begin + after + sep, sep)
				else:
					o.text(begin + after + sep, sep)
		
		if current != "":
			alignText(current, begin, first, after)
	
	def latex(self):
		lasttrigger = False

		for o in self.content:
			if isinstance(o, Trigger):
				if not lasttrigger:
					sys.stdout.write("\\begin{%s}\n" % itemize)
					lasttrigger = True
				
				sys.stdout.write("\\item ")
				o.latex()
				sys.stdout.write("\n")
			
			else:
				if lasttrigger:
					sys.stdout.write("\\end{%s}" % itemize)
					lasttrigger = False
				
				if isinstance(o, TextContent):
					sys.stdout.write(latex(o.text))
				elif isinstance(o, LaTeXContent):
					sys.stdout.write(o.tex)
				elif isinstance(o, SAClass):
					o.latex()
		
		if lasttrigger:
			sys.stdout.write("\\end{%s}" % itemize)

	def countType(self, _type):
		res = 0
		for o in self.content:
			if isinstance(o, Trigger):
				res += o.countType(_type)
			elif isinstance(o, SAClass):
				if o.classification == _type:
					res += 1
		return res


class TextContent(TriggerContent):
	"""Container for basic text"""
	
	def __init__(self, text):
		self.text = text

class LaTeXContent(TriggerContent):
	"""Container for LaTeX"""

	def __init__(self, tex):
		self.tex = tex

# Parse

def getBook(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	result = Book(root.find("./name").text)
	
	def extractForce(elem):
		force = Force(elem.get("name"))

		for e in elem:
			if e.tag == "assertive":
				force.assertive = True
			elif e.tag == "commissive":
				force.commissive = True
			elif e.tag == "declarative":
				force.declarative = True
			elif e.tag == "directive":
				force.directive = True
			elif e.tag == "expressive":
				force.expressive = True

		return force
	
	def extractClass(elem):
		result = SAClass(elem.get("type"))
		result.addText(elem.text)

		for e in elem:
			if e.tag == "tex":
				result.addLaTeX(e.text)
			if e.tag == "force":
				result.addForce(extractForce(e))
			result.addText(e.tail)
	
		return result
	
	def extractTrigger(elem):
		result = Trigger()
		result.addText(elem.text)
	
		for e in elem:
			if e.tag == "class":
				result.addContent(extractClass(e))
			elif e.tag == "trigger":
				result.addContent(extractTrigger(e))
			elif e.tag == "tex":
				result.addContent(LaTeXContent(e.text))
			result.addText(e.tail)
		
		return result
	
	# Processes
	for process in root.findall("./process"):
		name = process.find("./name")
		p = Process(name.text if name != None else None)
		result.addProcess(p)
	
		for trigger in process.findall("./trigger"):
			p.addTrigger(extractTrigger(trigger))
	
	return result
