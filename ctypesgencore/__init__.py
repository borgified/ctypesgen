#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

"""
Ctypesgencore is the module that contains the main body of ctypesgen - in fact,
it contains everything but the command-line interface.

ctypesgen's job is divided into three steps:

Step 1: Parse

Ctypesgen reads the input header files and parses them. It generates a list of
function, variable, struct, union, enum, constant, typedef, and macro
descriptions from the input files. These descriptions are encapsulated as
ctypesgen.descriptions.Description objects.

The package ctypesgen.parser is responsible for the parsing stage.

Step 2: Process

Ctypesgen processes the list of descriptions from the parsing stage. This is
the stage where ctypesgen resolves name conflicts and filters descriptions using
the regexes specified on the command line. Other processing steps take place
at this stage, too. When processing is done, ctypesgen finalizes which
descriptions will be included in the output file.

The package ctypesgen.processor is responsible for the processing stage.

Step 3: Print

Ctypesgen writes the descriptions to the output file, along with a header.

The package ctypesgen.printer is responsible for the printing stage.

There are three modules in ctypesgencore that describe the format that the
parser, processor, and printer modules use to pass information. They are:

* descriptions: Classes to represent the descriptions.

* ctypedecls: Classes to represent C types.

* expressions: Classes to represent an expression in a language-independent
format.
"""

__version__ = "1.0.1.dev8"
VERSION = __version__

__all__ = [
    "ctypedescs",
    "descriptions",
    "expressions",
    "messages",
    "options",
    "parser",
    "printer",
    "printer_python",
    "processor",
]

# Workhorse modules
import ctypesgencore.parser as parser
import parser
import ctypesgencore.processor as processor
import ctypesgencore.printer_python

#

try:
    import printer_json
except ImportError:
    pass

# Modules describing internal format
from ctypesgencore import descriptions
from ctypesgencore import ctypedescs
from ctypesgencore import expressions

# Helper modules
from ctypesgencore import messages
from ctypesgencore import options
from ctypesgencore import printer_python

printer = printer_python  # Default the printer to generating Python
