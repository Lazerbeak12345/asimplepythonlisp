LANG="en-us"
def printError(code):
    print(f"Error: {code}")
    print(errorCodes[LANG][code])
errorCodes={
        "en-us":{ # TODO translate this dictionary
            "noArgs":"I need another argument, representing the filename",
            "extraTerminator":"Extra list terminator found!",
            "missingEndParen":"Missing at least one list terminator",
            "mismachTerminator":"""List terminator does not match last list
    initializer""",
            "notDefined":"This variable is not defined:",
            "notWrittenYet":"""The code that handles this interpreter feature has
    not been written yet""",
            "notIdentInArg":"""The value supplied as an argument when defining a
    function was not an identifier""",
            }
        }
