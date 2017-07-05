# Evaluation of Interfaces and Triggers in ITIL

Today’s organizations are socio-technical systems in which human workers increasingly perform knowledge work.
Interactions between knowledge workers, clerks, and systems are essentially speech acts controlling the necessity and flow of activities in semi-structured and ad-hoc processes.
IT-support for knowledge work does not necessarily require any predefined process model, and often none is available.
To capture what is going on, a rising number of approaches for process modeling, analysis, and support classify interactions and derive process-related information.
The frequency and diversity of speech acts has only been examined within delimited domains, but not in the larger setting of a reference model covering different types of work and domains, multiple stakeholders, and interacting processes.
Therefore, we have investigated interactions in the IT Infrastructure Library (ITIL).
ITIL is a collection of predefined processes, functions, and roles that constitute best practices in the realm of IT service management (ITSM).
For ITIL-based processes, we demonstrate the importance, prevalence, and diversity of interactions in triggers,
and that further abstraction of interactions can improve the reusability of process patterns.
Hence, at least in ITSM, applying speech act theory bears great potential for process improvement.

This repository contains all raw information extracted from the core publications of ITIL for the paper:

> *Johannes Tenschert, Jana-Rebecca Rehse, Peter Fettke, and  Richard Lenz:*
> **Speech Acts in Actual Processes: Evaluation of Interfaces and  Triggers in ITIL.**
> In: The 10th Workshop on Social and Human Aspects of Business Process Management (BPMS2'17).
> (2017).

## Format
One XML file per book. A trigger can be attributed to more than one category.
One specific part of a text block is attributed to exactly one category.
This approach was sufficient for all five core publications.
Triggers can be nested to properly create lists, eg. for change management.
The DTD does not restrict nesting, but two levels did suffice for our analysis.

## Illocutionary Forces

The classification is available in the XML files as well.
See raw/triggers.dtd for data structure.
All XML tags of illocutionary points can be viewed as a flag.
If the empty tag for an illocutionary point is available, the flag is set to true.

## Interfaces

**TODO**

## Report

Generating the report is done with make (or make trigger.pdf).
There are options in config.py to enable/disable statistics and books.
The makefile executes extractClassification.py, extractForces.py, and adds LaTeX boilerplate (head.tex, middle.tex, tail.tex).

| Command         | Description                                                 |
| --------------- | ----------------------------------------------------------- |
| `make`          | Generate report                                             |
| `make clean`    | Clean this folder                                           |
| `make proper`   | Reset this folder                                           |
| `make checkdtd` | Check raw XML files for whether they adhere to triggers.dtd |
