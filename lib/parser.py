from lib.errorCodes import errorCodes
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
                    # TODO: make this a proper xor
                    # What we have here is effectively an xor
                    if not ((not(old=="(" and value==")")) and\
                        (not(old=="{" and value=="}")) and\
                        (not(old=="[" and value=="]"))):
                        parseStack[i-1].append(("list",parseStack.pop()))
                    else:
                        printError("mismachTerminator")
                        print("\t",parseStack,f"\n\tCurrent term {value}\n\tLast term {old}")
        else:
            if name=="#":#literals are weird
                if value=="f":
                    name="bool"
                    value=False
                elif value=="t":
                    name="bool"
                    value=True
            parseStack[i].append((name,value))
    if len(parseStack)>1:
        printError("missingEndParen")
        print("\t",parseStack)
    return parseStack[0]
