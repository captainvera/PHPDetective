import PatternParser

def getEntry(patterns):
    entries = []
    for pattern in patterns:
        for entry in pattern.getEntryPoints():
            if entry not in entries:
                entries.append(entry)
    
    return entries


def getVal(patterns):
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

