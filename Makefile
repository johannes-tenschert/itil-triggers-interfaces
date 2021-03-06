.PHONY: all clean checkdtd proper report interfaces
	
all: report interfaces

report: trigger.pdf

interfaces: interfaces.pdf

trigger.pdf: trigger.tex
	pdflatex -draftmode -interaction=batchmode trigger
	bibtex trigger
	pdflatex -draftmode -interaction=batchmode trigger
	pdflatex -synctex=1 -interaction=nonstopmode trigger

trigger.tex: config.py extractClassification.py extractForces.py raw/*.xml raw/comments.tex report-skel/head.tex report-skel/tail.tex report-skel/middle.tex report-skel/itil.bib
	cat report-skel/head.tex > trigger.tex
	python extractClassification.py >> trigger.tex
	cat report-skel/middle.tex >> trigger.tex
	python extractForces.py >> trigger.tex
	cat report-skel/tail.tex >> trigger.tex

clean:
	rm -f trigger.tex
	rm -f trigger.aux
	rm -f trigger.bbl
	rm -f trigger.blg
	rm -f trigger.log
	rm -f trigger.synctex.gz
	rm -f *.pyc
	rm -f interfaces/smaller.dot

proper: clean
	rm -f trigger.pdf
	rm -f interfaces.pdf

checkdtd:
	xmllint --valid --noout raw/ContinualServiceImprovement.xml raw/ServiceOperation.xml raw/ServiceTransition.xml raw/ServiceDesign.xml raw/ServiceStrategy.xml

interfaces.pdf: interfaces/smaller.dot
	neato -Tpdf -o interfaces.pdf interfaces/smaller.dot

interfaces/smaller.dot: interfaces/extract.py interfaces/raw.dot
	interfaces/extract.py < interfaces/raw.dot > interfaces/smaller.dot
