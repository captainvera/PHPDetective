import PatternParser
import sys


def getEntries(patterns):
    entries = []
    for pattern in patterns:
        for entry in pattern.getEntryPoints():
            if entry not in entries:
                entries.append(entry)
    
    return entries


def getVals(patterns):
    vals = []
    for pattern in patterns:
        for val in pattern.getSanitizingFunctions():
            if val not in vals:
                vals.append(val)
    return vals


def getSinks(patterns):
    sinks = []
    for pattern in patterns:
        for sink in pattern.getSensitiveSinks():
            if sink not in sinks:
                sinks.append(sink)

    return sinks

def printResults(slic, patterns):
    if(len(patterns > 0)):
        print("-----------------------")
        for pat in patterns:
            print(pat.vuln + " Vulnerability Detected")
        print()
        print("The vulnerability enters through: ")
        for entry in slic.dangerousEntryPoints:
            print(entry.name + " on line " + str(entry.line))
        print()
        print("Tainted Variables: ")
        for var in slic.variables:
            print(var.name + " on line " + str(var.line))
        print()
        print("Vulnerability is injected into the system in: ")
        for sink in slic.sensitiveSinks:
            print(sink.name + " on line " + str(sink.line))
        print("-----------------------")

    else:
        print("-----------------------")
        print("No Vulnerability Detected")
        print()
        print("Sanitization is done in:")
        for val in slic.validations:
            print(val.name + " on line " + str(val.line))
        

