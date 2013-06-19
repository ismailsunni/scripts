#!/usr/bin/env python
"""A script to download material from talktomeinkorean.com.
Please support them since they are really great.
You can read the way to support them in
http://www.talktomeinkorean.com/support/
"""

__author__ = 'Ismail Sunni'
__copyright__ = 'Ismail Sunni'
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'Ismail Sunni'
__email__ = 'imajimatika@gmail.com'
__status__ = 'Prototype'
__date__ = '19 June 2013'

import sys
import urllib

def download_audio(level, lesson, filename=None):
    source_file = ('http://media.libsyn.com/media/talktomeinkorean/'
                   'TTMIK-Lesson-L%sL%s.mp3') % (level, lesson)
    
    if filename is None:
        filename = ('TTMIK-Lesson-L%sL%s.mp3') % (level, lesson)
    
    # Simple download file
    # TO DO : Change to http://stackoverflow.com/a/9740603/1198772
    print '[+] Downloading audio level %s lesson %s' % (level, lesson)
    print urllib.urlretrieve(source_file, filename)
    print '[+] Saved to ' + filename

def download_pdf(level, lesson, filename=None):
    source_file = ('http://talktomeinkorean.com/pdf-files/'
                   'ttmik-l%sl%s.pdf') % (level, lesson)
        
    if filename is None:
        filename = ('ttmik-l%sl%s.pdf') % (level, lesson)
    
    # Simple download file
    # TO DO : Change to http://stackoverflow.com/a/9740603/1198772
    print '[+] Downloading pdf level %s lesson %s' % (level, lesson)
    print urllib.urlretrieve(source_file, filename)
    print '[+] Saved to ' + filename

def usage():
    print 'Usage: python talktomeinkorean.py [both/pdf/audio] [level] [lesson]'
    sys.exit()

def main():
    num_argv = len(sys.argv)
    if num_argv != 4:
        usage()
    # parameter
    files = sys.argv[1]
    level = sys.argv[2]
    lesson = sys.argv[3]
    print 'Parameters: %s, %s, %s' % (files, lesson, level)
    if files == 'both' or files == 'audio':
        download_audio(lesson, level)
    if files == 'both' or files == 'pdf':
        download_pdf(lesson, level)


if __name__ == '__main__':
    # download_pdf(1, 100)
    main()
