import sys
import getopt
import logging

logging.basicConfig( level=logging.DEBUG)

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

        """
        patterns = ParternParser.parse("sqlinjection.txt")

        slices = SliceParser.parse(inputfile)

        if(Matcher)
            print("Vulnerability found")
        else print("Program is ok")
        """


main(sys.argv[1:]);
