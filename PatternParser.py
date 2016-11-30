import os
import logging

logging.basicConfig( level=logging.ERROR)

def getChunks(data, n):
    """
    Divides the data in chunks of n lines (in this case, excluding \n)
    """
    chunks = []
    data = list(filter(('\n').__ne__, data))
    next_chunk = []

    for line in data:
        line = line.strip(' \n\t\r')

        logging.debug('N:',len(next_chunk))
        logging.debug('LINE:',line)

        if (len(next_chunk)==n):
            chunks.append(next_chunk)
            next_chunk = []

            logging.debug('\n----- END OF PATTERN -----\n')

        next_chunk.append(line)

        logging.debug('NEXT CHUNK:',next_chunk)

    chunks.append(next_chunk)
    logging.debug(chunks)
    return chunks

###################################################################

class PatternParser:
    folder = ''
    toParse = []
    known_patterns = []

    def __init__(self,folder):
        self.folder = folder
        for file in os.listdir(folder):
            self.toParse.append(file)

    def parse(self, file):
        """
        Parses an individual pattern file and adds it to the known patterns list
        """

        path = self.folder+'/'+file
        new_patterns = []
        logging.info('[>] Parsing all patterns in',file)

        raw_text = open(path,'r')
        lines = raw_text.readlines()
        patterns = getChunks(lines,4)
        for pattern in patterns:
            vuln = pattern[0]
            entry_points = pattern[1]
            san_functions = pattern[2]
            sens_sinks = pattern[3]

            new_pattern = Pattern(vuln,entry_points,san_functions,sens_sinks)
            new_patterns.append(new_pattern)

            logging.debug(new_pattern)

        raw_text.close()
        self.known_patterns += new_patterns

    def parseAll(self):
        """
        Parses all files to be parsed
        """
        for file in self.toParse:
            self.parse(file)

    def getKnownPatterns(self):
        """
        Returns a list of known patterns
        """
        return self.known_patterns

###################################################################

class Pattern:
    vuln = ''
    entry_points = []
    san_functions = []
    sens_sinks = []

    def __init__(self, vuln, entry_points, san_functions, sens_sinks):
        self.vuln = vuln
        self.entry_points = entry_points
        self.san_functions = san_functions
        self.sens_sinks = sens_sinks

    def getVuln(self):
        return self.vuln

    def getEntryPoints(self):
        return self.entry_points

    def getSanitizingFunctions(self):
        return self.san_functions

    def getSensitiveSinks(self):
        return self.sens_sinks

    def __str__(self):
        return '\n--------------------\n'+ \
                self.vuln+'\n'+ \
                str(self.entry_points)+'\n'+ \
                str(self.san_functions)+'\n'+ \
                str(self.sens_sinks) +'\n'+ \
                '--------------------'

###################################################################

"""
Utilization examples
"""

#creates a parser to parse all files in 'Patterns' folder
patParser = PatternParser('Patterns')

#parses all files
patParser.parseAll()

#gets a list of the patterns in those files
patterns = patParser.getKnownPatterns()
