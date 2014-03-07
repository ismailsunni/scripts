"""Simple script to add string from a list of string in external files.
"""

__author__ = 'ismailsunni'
__project_name = 'Scripts'
__filename = 'Crawler'
__date__ = '05/02/14'
__copyright__ = 'imajimatika@gmail.com'
__doc__ = ''

import sys
from pprint import pprint

def usage():
    print 'Usage:'
    print 'python add_string.py extra_string input_file [output_file]'


if __name__ == '__main__':
    if len(sys.argv) == 4:
        extra_string = sys.argv[1]
        input_file = sys.argv[2]
        output_file = sys.argv[3]
    elif len(sys.argv) == 3:
        extra_string = sys.argv[1]
        input_file = sys.argv[2]
        output_file = input_file
    else:
        usage()
        exit()

    try:
        f = open(input_file, 'r')
        input_strings = f.readlines()
        f.close()
    except Exception, e:
        print 'Error', e
        raise e

    output_strings = []
    for input_string in input_strings:
        if len(input_string) > 140 - len(extra_string) - 1:
            continue
        if input_string[-1] == '\n':
            input_string = input_string[:-1]
        if input_string[-1] == ' ':
            input_string += extra_string
        else:
            input_string += ' ' + extra_string
        output_strings.append(input_string)

    f = open(output_file, 'w')
    for output_string in output_strings:
        f.write("%s\n" % output_string)
    f.close()

