#!/usr/bin/env python3
#TODO seperate into multiple files
import sys
import math
from lib.errorCodes import printError
from lib.tokenizer import tokenizer
from lib.parser import parser
BUILTIN_RUNTIME_FUNCTIONS=[
        "define",
        "print",
        "printf",
        "substring",
        "string-append",
        "string-length",
        "string?",
        "sqrt",
        "+",
        "<",
        ">=",
        "number?",
        "equal?"
        ]
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
def printAsText(node,end="\n"):
    name,value=node
    if name=="int" or name=="dbString":
        print(value,end="")
    print(end,end="")
    #TODO: other types
def runner(tree,loud=False,s=[{}]):
    """Call a lisp tree (such as a file or a function)"""
    #s is the value stack (always push to the front!!)
    #print(s)
    lastValue=("list",[])
    lang=None
    for node in tree:
        name,value=node
        if name=="#" and value=="lang":
            lang=False
        elif lang==False:
            lang=value
        elif name=="ident":
            var=getVarFromStack(s,value)
            if var!=False and var!=True:
                if loud:
                    if var[0]=="lambda":
                        print(f"#<procedure:{value}>") # TODO: there's more than just procedures
                    else:
                        printTypedValue(var)
                        lastValue=var
                else:
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
                    #TODO: check that this is lazy loaded
                    newLayer={}
                    for index in range(len(expectedArgs)):
                        newLayer[expectedArgs[index][1]]=callArgs[index]
                    s.insert(0,newLayer)
                    lastValue=runner(var[1][1],False,s)
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
                            for item in newFuncArgs:
                                if item[0]!="ident":
                                    printError("notIdentInArg")
                                    printTypedValue(item)
                                    sys.exit(1)
                            #TODO: test scope
                            s[0][newFuncName]=("lambda",(newFuncArgs,newFuncBody))
                        else:
                            pass #TODO: print error
                    elif firstInList[1]=="print":
                        for item in a:#clunky, but allows more control of output
                            printTypedValue(runner([item],s=s),end="")
                    elif firstInList[1]=="printf":
                        strin=runner([a[0]],s=s)
                        if strin[0]!="dbString":
                            pass #TODO: print error
                        for item in a:#clunky, but allows more control of output
                            printAsText(runner([item],s=s),end="")
                    elif firstInList[1]=="substring":
                        strin=runner([a[0]],s=s)
                        if strin[0]!="dbString":
                            pass #TODO: print error
                        start=runner([a[1]],s=s)
                        if strin[0]!="int":
                            pass #TODO: print error
                        if start[1]>0:
                            pass #TODO: print error
                        if len(a)<3:
                            end=("int",len(strin))
                        else:
                            end=runner([a[2]],s=s)
                            if end[0]!="int":
                                pass #TODO: print error
                        lastValue=("dbString",strin[1][start[1]:end[1]])
                    elif firstInList[1]=="string-append":
                        out=""
                        for chunk in a:
                            strin=runner([chunk],s=s)
                            if strin[0]!="dbString":
                                pass #TODO: print error
                            out+=strin[1]
                        lastValue=("dbString",out)
                    elif firstInList[1]=="string-length":
                        strin=runner([a[0]],s=s)
                        if strin[0]!="dbString":
                            pass #TODO: print error
                        lastValue=("int",len(strin))
                    elif firstInList[1]=="string?":
                        strin=runner([a[0]],s=s)
                        lastValue=("bool",strin[0]=="dbString")
                    elif firstInList[1]=="number?":
                        intin=runner([a[0]],s=s)
                        lastValue=("bool",strin[0]=="int")
                    elif firstInList[1]=="equal?":
                        lastInt=None
                        for num in a:
                            intin=runner([a[0]],s=s)
                            if not lastInt:
                                lastInt=intin
                            elif not lastInt==intin:
                                lastValue=("bool",False)
                                break
                            else:
                                lastInt=intin
                        lastValue=("bool",True)
                    elif firstInList[1]=="sqrt":
                        intin=runner([a[0]],s=s)
                        if intin[0]!="int":
                            pass #TODO: print error
                        if intin[1]>0:
                            lastValue=("int",math.sqrt(intin[1]))
                        else:
                            lastValue=("int",complex(0,math.sqrt(-1*intin[1])))
                    elif firstInList[1]=="+":
                        total=0
                        for num in a:
                            intin=runner([a[0]],s=s)
                            if intin[0]!="int":
                                pass #TODO: print error
                            total+=intin[1]
                        lastValue=("int",total)
                    elif firstInList[1]=="<":
                        lastInt=None
                        for num in a:
                            intin=runner([a[0]],s=s)
                            if intin[0]!="int":
                                pass #TODO: print error
                            if not lastInt:
                                lastInt=intin
                            elif not lastInt<intin:
                                lastValue=("bool",False)
                                break
                            else:
                                lastInt=intin
                        lastValue=("bool",True)
                    elif firstInList[1]==">=":
                        lastInt=None
                        for num in a:
                            intin=runner([a[0]],s=s)
                            if intin[0]!="int":
                                pass #TODO: print error
                            if not lastInt:
                                lastInt=intin
                            elif not lastInt>=intin:
                                lastValue=("bool",False)
                                break
                            else:
                                lastInt=intin
                        lastValue=("bool",True)
                    else:
                        printError("notWrittenYet")
                        print(firstInList[1])
                        sys.exit(1)
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
    printTypedValue(outValue)
    #if outValue[0]=="list" and outValue[1]==[]:
    #    sys.exit(0)
    #sys.exit(outValue[1])

