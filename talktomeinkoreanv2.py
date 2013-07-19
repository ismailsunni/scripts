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

def mkdir(level, lesson):
    """Create directory TTMIK/level/lesson if not exist
    """
    dir_path = os.path.join('TTMIK', str(level), str(lesson))
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
    lesson_bs = get_page_soup(lesson_url, 'level%slesson%s.html' % (level,
    lesson))
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

def download_mp3(mp3_url, level, lesson):
    """Download a mp3 file from a link, and put it under TTMIK/level/lesson
    directory.
    """
    mkdir(level, lesson)
    local_path = get_local_path(level, lesson, 'mp3')
    print local_path
    urllib.urlretrieve(mp3_url, local_path)

def main():
    level = 7
    lesson = 30
    lesson_url = get_lesson_url(level, lesson)
    print lesson_url
    mp3_url = get_mp3_url(lesson_url, level, lesson)
    download_mp3(mp3_url, level, lesson)

if __name__ == '__main__':
    main()


