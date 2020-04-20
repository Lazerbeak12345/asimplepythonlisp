def tokenizer(filE):
    """Look through a given file, and return a list of tuples, first value type
    second is value"""
    tokens=[]
    mode="token"
    add=True # We don't know what the char is.
    currentToken=None # The current token, if it is multiple chars long
    validNumbers="0123456789" # All valid numbers at the index of their value
    validListEnds="()[]{}"
    validWhitespace=" \t\n\r"
    cantBeInIdent="()[]{}\",'`;#|\\"
    for line in filE:
        for char in line:
            # TODO: support 1/2 3.14 6.02e+23 1+2i 9999999999999999999999
            # TODO: Support #t #f
            # TODO: support backtabbed unicode ( "\u0022" is '"'
            # TODO: support escaping doublequotes like this: "\""
            # TODO: support for #lang
            if mode=="int": # TODO handle for floats and other numbers
                if char in validWhitespace or\
                        char in cantBeInIdent:
                    add=True
                elif char in validNumbers:
                    currentToken=(currentToken*10)+validNumbers.find(char)
                elif currentToken==-1:
                    mode="ident"
                    currentToken="-"+char
                else:
                    add=True
            elif mode=="ws":
                if not char in validWhitespace:
                    add=True
            elif mode=="ident":
                if char in validWhitespace or\
                        char in cantBeInIdent:
                    add=True
                else:
                    currentToken+=char
            elif mode=="dbString":
                if len(currentToken)>1 and currentToken[-1]=='"':
                    add=True
                    currentToken=currentToken[0:-1]
                    #TODO: do mode="string"
                elif len(currentToken)>0 and currentToken[-1]=="\\":
                    currentToken=currentToken[0:-1] # Remove the backslash
                    if char=="n":
                        currentToken+="\n"
                    elif char=="\"":
                        currentToken+="\""
                    else:
                        pass #TODO throw error
                else:
                    currentToken+=char
            elif mode=="comment":
                if char=='\n':
                    add=True
            elif mode=="#":
                #TODO: add more than just identifier type # things
                if char in validListEnds or\
                    char in validNumbers or\
                    char in validWhitespace:
                        add=True
                else:
                    currentToken+=char
            if add:# We are searching
                if currentToken!=None:
                    tokens.append((mode,currentToken))
                mode="token"
                currentToken=None
                add=False
                if char in validNumbers or char=="-":
                    mode="int"
                    if char=="-":
                        currentToken=-1
                    else:
                        currentToken=validNumbers.find(char)
                elif char in validWhitespace:
                    mode="ws"
                elif char in validListEnds:
                    mode="listEnd"
                    currentToken=char
                    add=True # We can add it right away
                elif char=='"':
                    mode="dbString"
                    currentToken=""
                elif char==";":
                    mode="comment"
                elif char=="#":
                    mode="#"
                    currentToken=""
                else:
                    mode="ident"
                    currentToken=char
    return tokens
