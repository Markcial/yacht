import sys
from optparse import OptionParser
from code import InteractiveConsole

parser = OptionParser()
parser.add_option(
    "-a", "--append", action="store_true",
    dest="append", help="appends to FILE instead of writing it"
)
parser.add_option(
    "-f", "--file", dest="filename",
    help="writes the hosts discovered to FILE", metavar="FILE"
)
parser.add_option(
    "-v", "--verbose",
    dest="verbose", action="store_true"
)


def list():
    print 'list'


def launcher():
    (options, args) = parser.parse_args()
    print options, args
    print str(parser)

if __name__ == '__main__':
    launcher()