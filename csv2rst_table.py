#!/usr/bin/env python
"""A script to convert csv table to rst table.
"""

__author__ = 'Ismail Sunni'
__copyright__ = 'Ismail Sunni'
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Ismail Sunni'
__email__ = 'imajimatika@gmail.com'
__status__ = 'Prototype'
__date__ = '7 March 2014'


import sys
import re

def usage():
    print 'Wrong command'
    print 'Usage: python csv2rst_table.py [input_file]'


def main(input_file, output_file=None, header=True, csv_sep=';', rst_sep=' | '):
    if output_file is None:
        output_file = input_file[:-3] + 'rst'
    try:
        f = open(input_file, 'r')
        lines = f.readlines()
        f.close()
    except Exception, e:
        print 'Error', e
        raise e
    if header:
        header_sep = re.sub('[^' + csv_sep + ']', '-', lines[0]) + '\n'
        lines = lines[:1] + [header_sep] + lines[1:]
    result = ''
    for line in lines:
        line = line.replace(csv_sep, rst_sep)
        result += line
    try:
        f = open(output_file, 'wt')
        f.write(result)
        f.close()
    except Exception, e:
        print 'Error', e
        raise e

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        exit()
    input_file = sys.argv[1]
    main(input_file)