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

def get_mp3_url(lesson_url, level, lesson):
    """Return mp3 url from a page url.
    """
    mkdir('htmlpage', level, lesson)
    temp_html_file = 'level%slesson%s.html' % (level, lesson)
    temp_html_page = os.path.join('htmlpage', str(level), str(lesson),
                                  temp_html_file)
    print lesson_url
    lesson_bs = get_page_soup(lesson_url, temp_html_page)
    lesson_a = lesson_bs.findAll('a')
    mp3_links = []
    for a in lesson_a:
        if 'mp3' in str(a):
            mp3_links.append(a.get('href'))

    # Assume the first link with mp3 is the correct one 
    return mp3_links[0]

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
        print 'already exist, do not download'
        return
    urllib.urlretrieve(file_url, local_path)
    print 'Done'

def main():
    for level in xrange(1, 8):
        for lesson in xrange(1, 31):
           lesson_url = get_lesson_url(level, lesson)
           mp3_url = get_mp3_url(lesson_url, level, lesson)
           print 'mp3_url', mp3_url
           try:
               download(mp3_url, level, lesson, 'mp3')
           except Exception, e:
                print level, lesson, e

if __name__ == '__main__':
    main()


