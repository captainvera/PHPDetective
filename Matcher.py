import logging
import SliceParser

logger = logging.getLogger("matchLogger")
logger.setLevel(logging.WARNING)

def match(slic, patterns):
    res = []
    entryPointNames = []
    sinkNames = []

    for entry in slic.entryPoints:
        entryPointNames.append(entry.name)
    for sink in slic.sensitiveSinks:
        sinkNames.append(sink.name)

    for patt in patterns:
        if(set(entryPointNames).isdisjoint(patt.entry_points) == False and set(sinkNames).isdisjoint(patt.sens_sinks) == False):
            logger.info("Found Vulnerability")
            logger.info(patt.vuln)
            res.append(patt)

    return res

