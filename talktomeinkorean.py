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

def max_lesson(level):
    """Return maximum lesson for a level.
    Currently I write it hard code. Ahaha.
    """
    if level == 1:
        return 25
    elif 1 < level <= 7:
        return 30
    else:
        return 0

def download_audio(level, lesson=None, filename=None):
    """Download single file of audio.
    """

    source_file = ('http://media.libsyn.com/media/talktomeinkorean/'
                   'TTMIK-Lesson-L%sL%s.mp3') % (level, lesson)
    
    if filename is None:
        filename = ('TTMIK-Lesson-L%sL%s.mp3') % (level, lesson)
 
    # Simple download file
    # TO DO : Change to http://stackoverflow.com/a/9740603/1198772
    print '[+] Downloading audio level %s lesson %s' % (level, lesson)
    print urllib.urlretrieve(source_file, filename)
    print '[+] Saved to ' + filename

def download_audios(level):
    """Download multiple files of audio in a level.
    """
    num_lesson = max_lesson(level)
    for lesson in xrange(num_lesson):
        download_audio(level, lesson + 1)

def download_pdf(level, lesson, filename=None):
    """Download single file of pdf.
    """
    source_file = ('http://talktomeinkorean.com/pdf-files/'
                   'ttmik-l%sl%s.pdf') % (level, lesson)
        
    if filename is None:
        filename = ('ttmik-l%sl%s.pdf') % (level, lesson)
    
    # Simple download file
    # TO DO : Change to http://stackoverflow.com/a/9740603/1198772
    print '[+] Downloading pdf level %s lesson %s' % (level, lesson)
    print urllib.urlretrieve(source_file, filename)
    print '[+] Saved to ' + filename

def download_pdfs(level):
    """Download multiple files of pdf in a level.
    """
    num_lesson = max_lesson(level)
    for lesson in xrange(num_lesson):
        download_pdf(level, lesson + 1)

def usage():
    print 'Usage: python talktomeinkorean.py [both/pdf/audio] [level] [optional lesson]'
    sys.exit()

def main():
    num_argv = len(sys.argv)
    if num_argv > 4:
        usage()
    elif num_argv == 4:
        # parameter
        files = sys.argv[1]
        level = sys.argv[2]
        lesson = sys.argv[3]
        print 'Parameters: %s, %s, %s' % (files, lesson, level)
        if files == 'both' or files == 'audio':
            download_audio(lesson, level)
        if files == 'both' or files == 'pdf':
            download_pdf(lesson, level)
    elif num_argv == 3:
        # parameter
        files = sys.argv[1]
        level = sys.argv[2]
        print 'Parameters: %s, %s' % (files, lesson)
        if files == 'both' or files == 'audio':
            download_audios(lesson)
        if files == 'both' or files == 'pdf':
            download_pdfs(lesson)


if __name__ == '__main__':
    # download_pdf(1, 100)
    # main()
    download_audios(1)
