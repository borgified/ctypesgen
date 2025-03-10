import os
import sys
import six

try:
    import StringIO
except ImportError:
    import io as StringIO
if not six.PY2:
    import importlib
    from importlib import reload

import optparse
import glob

sys.path.append(".")  # Allow tests to be called from parent directory with Python 2.6
sys.path.append("..")
import ctypesgencore
from ctypesgencore.parser import parse

"""ctypesgentest is a simple module for testing ctypesgen on various C constructs. It consists of a
single function, test(). test() takes a string that represents a C header file, along with some
keyword arguments representing options. It processes the header using ctypesgen and returns a tuple
containing the resulting module object and the output that ctypesgen produced."""

# set redirect_stdout to False if using console based debugger like pdb
redirect_stdout = True


def test(header, **more_options):

    assert isinstance(header, six.string_types)
    with open("temp.h", "w") as fd:
        fd.write(header)

    options = ctypesgencore.options.get_default_options()
    options.headers = ["temp.h"]
    for opt in more_options:
        setattr(options, opt, more_options[opt])

    if redirect_stdout:
        # Redirect output
        sys.stdout = StringIO.StringIO()

    # Step 1: Parse
    descriptions = parse(options.headers, options)

    # Step 2: Process
    ctypesgencore.processor.process(descriptions, options)

    # Step 3: Print
    ctypesgencore.printer.WrapperPrinter("temp.py", options, descriptions)

    if redirect_stdout:
        # Un-redirect output
        output = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = sys.__stdout__
    else:
        output = ""

    if six.PY2:
        # Load the module we have just produced
        module = __import__("temp")
    else:
        module = importlib.import_module("temp")
    reload(module)

    return module, output


def cleanup(filepattern="temp.*"):
    fnames = glob.glob(filepattern)
    for fname in fnames:
        os.unlink(fname)
