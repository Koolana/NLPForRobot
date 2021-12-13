import sys
import re

def getConsoleArgs():
    """
    Returns a dictionary of arguments passed to through the CLI.
    """

    args = {}

    for arg in sys.argv[1:]:
        var = re.search('\-\-([A-Za-z]*)', arg) # optional value assignment
        var = var.group(1)
        value = re.search('\=(.*)', arg)
        value = value.group(1) if value else None
        args[var] = value

    return args
