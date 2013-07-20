#!/usr/bin/env python
"""A script to download material from talktomeinkorean.com.
Please support them since they are really great.
You can read the way to support them in
http://www.talktomeinkorean.com/support/
"""

__author__ = 'Ismail Sunni'
__copyright__ = 'Ismail Sunni'
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Ismail Sunni'
__email__ = 'imajimatika@gmail.com'
__status__ = 'Prototype'
__date__ = '16 July 2013'

import urllib
import urllib2
import os
from BeautifulSoup import BeautifulSoup

URL_BASE_CURRICULUM = 'http://www.talktomeinkorean.com/curriculum'


def mkdir(pardir, level, lesson):
    """Create directory pardir/level/lesson if not exist
    There are two known pardir, htmlpage and TTMIK
    htmlpage is used for storing temporary htmlpage
    TTMIK is used for storing mp3 and pdf file
    """
    dir_path = os.path.join(pardir, str(level), str(lesson))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def is_valid(level, lesson):
    """Check if a level and lesson is valid
    """
    if level == 1 and 0 < lesson < 26:
        return True
    if 1 < level < 8 and 0 < lesson < 31:
        return True
    return False

def get_index(level, lesson):
    """Return index from level and lesson
    """
    if level == 1:
        return (level - 1) * 30  + lesson
    else:
        return (level - 1) * 30  + lesson - 5

def get_page_soup(url, local_html='page.html'):
    """Download a page and return a BeautifulSoup object of the html"""
    if not os.path.exists(local_html):
        urllib.urlretrieve(url, local_html)
    html = ""
    with open(local_html) as html_file:
        for line in html_file:
            html += line
    return BeautifulSoup(html)


def get_lesson_url(level, lesson):
    """Return url for a level and a lesson
    """
    if not is_valid(level, lesson):
        return None

    curriculum = get_page_soup(URL_BASE_CURRICULUM, 'curriculum.html')
    curriculum_a = curriculum.findAll('a')
    list_link = []
    for a in curriculum_a:
        if ('Lesson ' in str(a) or 'Lesosn ' in str(a)) and 'target="_blank"' in str(a):
            list_link.append(a.get('href'))
    index = get_index(level, lesson)
    return list_link[index - 1]

def get_file_url(lesson_url, level, lesson, file_type):
    """Return file url from a page url.
    file type: mp3 or pdf
    """
    mkdir('htmlpage', level, lesson)
    temp_html_file = 'level%slesson%s.html' % (level, lesson)
    temp_html_page = os.path.join('htmlpage', str(level), str(lesson),
                                  temp_html_file)
    lesson_bs = get_page_soup(lesson_url, temp_html_page)
    lesson_a = lesson_bs.findAll('a')
    file_urls = []
    for a in lesson_a:
        if file_type in str(a):
            file_urls.append(a.get('href'))

    # Assume the first link with file_type is the correct one 
    return file_urls[0]

def get_local_path(level, lesson, type_file):
    """Return a file path to a file
    """
    filename =  'level%slesson%s.%s' % (level, lesson, type_file)
    return os.path.join('TTMIK', str(level), str(lesson), filename) 

def download(file_url, level, lesson, type_file):
    """Download a file from a link, and put it under TTMIK/level/lesson
    directory.
    """
    mkdir('TTMIK', level, lesson)
    local_path = get_local_path(level, lesson, type_file)
    print 'Downloading %s to %s' % (file_url, local_path)
    if os.path.exists(local_path):
        print 'Already exist, not downloading'
        return
    urllib.urlretrieve(file_url, local_path)
    print 'Done'

def download2(file_url, level, lesson, type_file):
    """Download a file from a link, and put it under TTMIK/level/lesson
    directory. With "progress bar"
    source : http://stackoverflow.com/a/22776/1198772 
    """
    mkdir('TTMIK', level, lesson)
    local_path = get_local_path(level, lesson, type_file)
    if os.path.exists(local_path):
        print 'Already exist, not downloading'
        return
    u = urllib2.urlopen(file_url)
    f = open(local_path, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (local_path, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

def get_file(level, lesson, file_type):
    """Wrap method to download file
    """
    msg = 'level: %s; lesson: %s; file type: %s' % (level, lesson, file_type)
    print 'Processing ' + msg
    lesson_url = get_lesson_url(level, lesson)
    if lesson_url is None:
        print 'Lesson URL is None'
        return
    if file_type in ['mp3', 'pdf']:
        file_url = get_file_url(lesson_url, level, lesson, file_type)
        try:
            download2(file_url, level, lesson, file_type)
        except Exception, e:
            print 'Exception ' + str(e) +  ' occurs for ' + msg
    else:
        print 'File type %s is not recognized.' % file_type


def main():
    for level in xrange(1, 2):
        for lesson in xrange(1, 31):
            get_file(level, lesson, 'mp3')

if __name__ == '__main__':
    main()


