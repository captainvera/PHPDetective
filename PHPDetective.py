import sys
import getopt
import logging
import PatternParser
import utilities
import SliceParser
import Matcher

logging.basicConfig( level=logging.WARNING)

def main(argv):

    inputfile = '';

    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        logging.error('PHPDetective.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logging.info('PHPDetective.py -i <inputfile>')
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            inputfile = arg;
            logging.debug('Input file is %s' % inputfile)

    patParser = PatternParser.PatternParser('Patterns')

    patParser.parseAll()

    patterns = patParser.getKnownPatterns()

    entryPoints = utilities.getEntries(patterns)
    validation = utilities.getVals(patterns)
    sensitiveSinks = utilities.getSinks(patterns)

    slic = SliceParser.fileParser(inputfile, entryPoints, validation, sensitiveSinks)

    patt = Matcher.match(slic, patterns)

    utilities.printResults(slic, patt)

main(sys.argv[1:]);
