#!/usr/bin/env python3
import sys
errorCodes={ # TODO translate this dictionary
        "noArgs":"I need another argument, representing the filename",
        "extraTerminator":"Extra list terminator found!",
        "missingEndParen":"Missing at least one list terminator",
        "mismachTerminator":"List terminator does not match last list initializer",
        "notDefined":"This variable is not defined:",
        }
def printError(code):
    print(f"Error: {code}")
    print(errorCodes[code])
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
    for line in filE:
        for char in line:
            # TODO: support 1/2 3.14 6.02e+23 1+2i 9999999999999999999999
            # TODO: Support #t #f
            # TODO: support backtabbed unicode ( "\u0022" is '"'
            # TODO: support escaping doublequotes like this: "\""
            # TODO: support for #lang
            if mode=="int": # TODO handle for floats and other numbers
                if char in validNumbers:
                    currentToken=(currentToken*10)+validNumbers.find(char)
                else:
                    add=True
            elif mode=="ws":
                if not char in validWhitespace:
                    add=True
            elif mode=="ident":
                if char in validListEnds or\
                    char in validNumbers or\
                    char in validWhitespace:
                        add=True
                else:
                    currentToken+=char
            elif mode=="dbString":
                if len(currentToken)>1 and currentToken[-1]=='"':
                    add=True
                    currentToken=currentToken[0:-1]
                else:
                    currentToken+=char
            elif mode=="comment":
                if char=='\n':
                    add=True
            if add:# We are searching
                if currentToken!=None:
                    tokens.append((mode,currentToken))
                mode="token"
                currentToken=None
                add=False
                if char in validNumbers:
                    mode="int"
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
                else:
                    mode="ident"
                    currentToken=char
    return tokens
def parser(tokens):
    parseStack=[[]]
    listTypeStack=[]
    for token in tokens:
        name,value=token
        i=len(parseStack)-1
        if name=="listEnd":
            if value=="(" or value=="[" or value=="{":
                parseStack.append([])
                listTypeStack.append(value)
            else:
                if i==0:
                    printError("extraTerminator")
                    print("\t",parseStack)
                else:
                    old=listTypeStack.pop() 
                    # What we have here is effectively an xor
                    if not ((not(old=="(" and value==")")) and\
                        (not(old=="{" and value=="}")) and\
                        (not(old=="[" and value=="]"))):
                        parseStack[i-1].append(("list",parseStack.pop()))
                    else:
                        printError("mismachTerminator")
                        print("\t",parseStack,f"\n\tCurrent term {value}\n\tLast term {old}")
        else:
            parseStack[i].append((name,value))
    if len(parseStack)>1:
        printError("missingEndParen")
        print("\t",parseStack)
    return parseStack[0]
BUILTIN_RUNTIME_FUNCTIONS=["define","print","substring"]
def getVarFromStack(s,name):
    """
    Get the tuple value of a variable from the stack

    return the the in-memory type tuple if it, or if it isn't in the stack
    then return a true if it's a builtin, false if it isn't
    """
    for layer in s:
        if name in layer:
            return layer[name]
    return name in BUILTIN_RUNTIME_FUNCTIONS
def printTypedValue(node,sep=" ",innerSep=" ",end=None,file=None,flush=None):
    name,value=node
    if name=="int" or name=="ident":
        print(value,end=end,file=file,flush=flush)
    elif name=="dbString":
        print('"',value.replace("\"","\\\""),'"',sep="",end=end,file=file,flush=flush)
    elif name=="list":
        print("(",end="")
        first=True
        for item in value:
            if first:
                first=False
            else:
                print(sep,end="")
            printTypedValue(item,sep=innerSep,innerSep=innerSep+sep,end="",file=file,flush=False)
        print(")",end=end)
def printAsText(node):
    name,value=node
    if name=="int" or name=="dbString":
        print(value)
    #TODO: other types
def runner(tree,loud=False,s=[{}]):
    """Call a lisp tree (such as a file or a function)"""
    #s is the value stack (always push to the front!!)
    #print(s)
    lastValue=("list",[])
    for node in tree:
        name,value=node
        if name=="ident":
            var=getVarFromStack(s,value)
            if var!=False and var!=True:
                if loud:
                    printTypedValue(var)
                lastValue=var
            elif not var:
                printError("notDefined")
                print(value)
                sys.exit(1)
            elif loud:
                print(f"#<procedure:{value}>") # TODO: there's more than just procedures
        elif name=="list": # We need to "run" this code (sortof)
            firstInList=value[0]
            if firstInList[0]=="ident" or firstInList[0]=="dbString":
                var=getVarFromStack(s,firstInList[1])
                if var!=False and var!=True:
                    if var[0]!="lambda":
                        pass #TODO throw error
                    callArgs=value[1:]
                    expectedArgs=var[1][0]
                    if len(callArgs)>len(expectedArgs):
                        pass #TODO throw error (more args than expected)
                    elif len(callArgs)<len(expectedArgs):
                        pass #TODO throw error (less args than expected)
                    newLayer={}
                    for index in range(len(expectedArgs)):
                        newLayer[expectedArgs[index][1]]=callArgs[index]
                    s.insert(0,newLayer)
                    runner(var[1][1],False,s)
                    s.pop(0)
                elif not var:
                    printError("notDefined")
                    print(firstInList[1])
                    sys.exit(1)
                else:
                    a=value[1:]
                    if firstInList[1]=="define":
                        if a[0][0]=="ident":
                            s.insert(0,{})
                            s[1][a[0][1]]=runner([a[1]],s=s)
                            #print(s)
                            s.pop(0)
                        elif a[0][0]=="list":
                            if not a[0][1][0][0]=="ident":
                                pass #TODO: print error
                            newFuncName=a[0][1][0][1]
                            newFuncArgs=a[0][1][1:]
                            newFuncBody=a[1:]
                            #TODO: test scope
                            s[0][newFuncName]=("lambda",(newFuncArgs,newFuncBody))
                        else:
                            pass #TODO: print error
                    elif firstInList[1]=="print":
                        for item in a:#clunky, but allows more control of output
                            printAsText(runner([item],s=s))
                    elif firstInList[1]=="substring":
                        print("substring",s)
                    else:
                        pass #TODO: print error
        else:
            if loud:
                printTypedValue(node)
            lastValue=node
    return lastValue
if __name__ == '__main__':
    if len(sys.argv) < 2:
        printError("noArgs")
        sys.exit(1)
    filE=open(sys.argv[1])
    outValue=runner(parser(tokenizer(filE)),loud=True)
    if outValue[0]=="list" and outValue[1]==[]:
        sys.exit(0)
    sys.exit(outValue[1])

