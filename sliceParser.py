import re
import logging

#Lists of possible EP/val/sink
possibleEp = []
possibleVal = []
possibleSink = []

#Lists of found things
foundEntryPoints = []
foundValidations = []
foundSensitiveSinks = []
foundVariables = []

logger = logging.getLogger("mylog")
logger.setLevel(logging.WARNING)

class Slice:
    entryPoints = []
    validations = []
    sensitiveSinks = []
    variables = []

    def __init__(self, entryPoints, validations, sensitiveSinks, variables, dangEntry):
        self.entryPoints = entryPoints
        self.dangerousEntryPoints = dangEntry
        self.validations = validations
        self.sensitiveSinks = sensitiveSinks
        self.variables = variables

    def getItems(self):
    	print("EntryPoints: ")
    	for x in range(len(self.entryPoints)):
    		print("Entry %d: %s" % (x,self.entryPoints[x].name))
    	print("SensitiveSinks: ")
    	for x in range(len(self.sensitiveSinks)):
    		print("Sink %d: %s" % (x,self.sensitiveSinks[x].name))
    	print("Sanitization: ")
    	for x in range(len(self.validations)):
    		print("Entry %d: %s" % (x,self.validations[x].name))
    	print("Variables: ")
    	for x in range(len(self.variables)):
    		print("Entry %d: %s" % (x,self.variables[x].name))

class EntryPoint:
    line = 0
    name = ''

    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.__dangerous = False
        self.sanitized = False

    def setDangerous(self, boolean):
        logger.debug("Dangerous set to -> " + str(boolean))
        if(self.sanitized == False):
            self.__dangerous = boolean
    
    def isDangerous(self):
        return self.__dangerous

    def sanitize(self):
        self.__dangerous = False
        self.sanitized = True

    def unSanitize(self):
        self.sanitized = False

class Variable:
    name = ''
    line = 0
    ancestors = []
    dangerous = False
    sanitized = False

    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.ancestors = []
        self.dangerous = False
        self.sanitized = False

    def setDangerous(self, boolean):
        if(self.sanitized == False):
            self.dangerous = boolean;
        
            if(len(self.ancestors) > 0):
                for ancestor in self.ancestors:
                    ancestor.setDangerous(boolean)

    def addAncestor(self, variables):
        self.ancestors.extend(variables);
    
    def sanitize(self):
        if(len(self.ancestors) > 0):
            for ancestor in self.ancestors:
                ancestor.setDangerous(False)

        self.ancestors = []
        self.dangerous = False
        self.sanitized = True

    def unSanitize(self):
        self.sanitized = False

"""
a = $_GET
b = a
c = b
d = c
mysqlQuery(d)
"""


class Sink:
    line = 0
    name = ''

    def __init__(self, name, line):
        self.name = name;
        self.line = line;

class Validation:
    line = 0
    name = ''

    def __init__(self, name, line):
        self.name = name;
        self.line = line;


def fileParser(fileName, entry, vali, sinks):
        global possibleEp 
        global possibleVal
        global possibleSink
        global foundVariables
        global foundSensitiveSinks
        global foundValidations
        global foundEntryPoints


        possibleEp = entry
        possibleVal = vali
        possibleSink = sinks

	#Insert FileName
        logger.debug("File Name : " + fileName)

	#Open fileName
        fo = open(fileName, "r")
        logger.debug("Is File Closed? " + str(fo.closed))

	#Read its content to a list
        lines = fo.readlines()
        
        #Variable to store treated input
        content = []
        temp_line = ''

        content = handleLines(lines)

        for i in range(len(content)):
            #search for the different types of objects
            foundSensitiveSinks.extend(getSinks(content[i], i+1))
            foundEntryPoints.extend(getEntryPoints(content[i], i+1))
            foundValidations.extend(getValidations(content[i], i+1))
            foundVariables.extend(getVariables(content[i], i+1))

        dangerousVars = []
        for variable in foundVariables:
            if(variable.dangerous == True):
                logger.info("[Ending] Dangerous Variable -> " + variable.name)
                dangerousVars.append(variable)

        dangerousEntries = []
        for entry in foundEntryPoints:
            if(entry.isDangerous() == True):
                logger.info("[Ending] Dangerous Entry -> " + entry.name)
                dangerousEntries.append(entry)
            else:
                logger.info("[Ending] Entry point -> " + entry.name + " with dangerous: " + str(entry.isDangerous()))

        for sanitization in foundValidations:
            logger.info("[Ending] Validation -> " + sanitization.name)

        for sink in foundSensitiveSinks:
            logger.info("[Ending] Sink -> " + sink.name)

    

        return Slice(foundEntryPoints, foundValidations, foundSensitiveSinks, dangerousVars, dangerousEntries)


#Find sinks in this line
def getSinks(line, lineNumber):
    logger.debug("[Function]->getSinks")
    result = []
    for sink in possibleSink:
        if sink in line:
            logger.debug("Found sink -> " + sink)
            sinkObj = Sink(sink, lineNumber)
            result.append(sinkObj)
            insideSink(line, sinkObj)

    return result;

def getVariables(line, lineNumber):
    logger.debug("[Function]->getVariable")
    result = []
    if "=" in line:
        logger.debug("Assignment in line:" + str(lineNumber))

        rightSide = []
        #has anything(only entries could have been) been found on this line?
        for entry in foundEntryPoints:
            if(entry.line == lineNumber):
                logger.debug("Entry on right side of assignment")
                rightSide.append(entry)

        #has it got another variable on this line?
        for var in foundVariables:
            if var.name in line:
                logger.debug("Variable on right side of assignment")
                rightSide.append(var)

        if(rightSide != []):
            var = line[line[:line.find("=")].find("$"):line.find("=")].rstrip()
            for obj in rightSide:
                if(var != ''):
                    logger.debug("Found Variable -> " + var)
                    varObj = Variable(var, lineNumber)
                    if(obj.sanitized == True):
                        varObj.sanitize()
                    else: 
                        varObj.unSanitize()
                    
                    varObj.addAncestor([obj])
                    result.append(varObj)

    return result

def getEntryPoints(line, lineNumber):
    logger.debug("[Function]->getEntryPoints")
    result = []
    for entry in possibleEp:
        if entry in line:
            logger.debug("Found Entry -> " + entry)
            entryObj = EntryPoint(entry, lineNumber)
            result.append(entryObj)

    return result;

def getValidations(line, lineNumber):
    logger.debug("[Function]->getValidations")
    result = []
    for val in possibleVal:
        if val in line:
            logger.debug("Found Validation -> " + val)
            valObj = Validation(val, lineNumber)
            result.append(valObj)
            insideValidation(line, valObj)
    return result

#What's going inside the sink? A dangerous variable? An Entry Point?
def insideSink(line, sink):

    global foundVariables
    logger.debug("[Function]->insideSink")

    sinkIndex = line.rfind(sink.name)

    if (sinkIndex == -1):
        logger.error("[ERROR] no sink:" + sink.name + " was found! What am I doing here?")

    else:
        entryPoints = getEntryPoints(line[sinkIndex:], sink.line)
        foundEntryPoints.extend(entryPoints)

        if(entryPoints == []):
            var = findVariable(line[sinkIndex:])
            if(var != None):
                var.setDangerous(True)
        else: 
            if(len(entryPoints) == 1):
                logger.debug("FOUND DANGEROUS ENTRY_POINT!!! ->" + entryPoints[0].name);
                entryPoints[0].setDangerous(True)
            else:
                for entry in entryPoints:
                    logger.debug("ENTRY_POINT->" + entry.name);
                    entry.setDangerous(True)

def findVariable(line):
    for var in foundVariables:
        if var.name in line:
            logger.debug("FOUND DANGEROUS VAR!!! ->" + var.name);
            if(len(var.ancestors) > 0):
                logger.debug("Originates on -> " + var.ancestors[0].name)
            return var
    return None

def insideValidation(line, val):
    global foundVariables
    logger.debug("[Function]->insideValidation")

    valIndex = line.rfind(val.name)

    if (valIndex == -1):
        logger.error("[ERROR] no validation:" + val.name + " was found! What am I doing here?")

    else:
        entryPoints = getEntryPoints(line[valIndex:], val.line)
        foundEntryPoints.extend(entryPoints)

        if(entryPoints == []):
            var = findVariable(line[valIndex:])
            if(var != None):
                var.sanitize();
        else: 
            if(len(entryPoints) == 1):
                logger.debug("sanitization :D !!! ->" + entryPoints[0].name);
                entryPoints[0].sanitize()
            else:
                for entry in entryPoints:
                    logger.debug("entry point->" + entry.name);
                    entry.sanitize()
        

def handleLines(lines):
    content = []
    temp_line = ''
    #Get rid of lines with no ; (they aren't the full line) The if is because there's a XSS slice without ;
    if(len(lines) != 1):
        for line in lines:
            if line.rstrip().endswith(';'):
                if(temp_line != ''):
                    temp_line += line.rstrip()
                    content.append(temp_line)
                    logger.debug("Multiple lines added to file: \"" + temp_line + "\"")
                    temp_line = ''
                content.append(line.rstrip())
                logger.debug("Line added to file: \"" + line.rstrip() + "\"")
            elif line.rstrip().endswith(">"):
                content.append(line.rstrip())

            else:
                temp_line += line.rstrip();
    else: 
        logger.debug("File only has 1 line : \"" + lines[0] + "\"")
        content = lines;

    return content

#TODO::XXX:: mysql_query(sanitize(entry_point))

