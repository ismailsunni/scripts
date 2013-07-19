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

def get_page_soup(url):
    """Download a page and return a BeautifulSoup object of the html"""
    if not os.path.exists('page.html'):
        urllib.urlretrieve(url, "page.html")
    html = ""
    with open("page.html") as html_file:
        for line in html_file:
            html += line
    return BeautifulSoup(html)


def get_lesson_url(level, lesson):
    """Return url for a level and a lesson
    """
    if not is_valid(level, lesson):
        return None

    curriculum = get_page_soup(URL_BASE_CURRICULUM)
    curriculum_a = curriculum.findAll('a')
    list_link = []
    for a in curriculum_a:
        if ('Lesson ' in str(a) or 'Lesosn ' in str(a)) and 'target="_blank"' in str(a):
            list_link.append(a.get('href'))
    index = get_index(level, lesson)
    return list_link[index - 1]

def get_mp3_url(page_url):
    """Return mp3 url from a page url.
    """
    lesson_page = get_page_soup()

def main():
    print get_lesson_url(7, 30)

if __name__ == '__main__':
    main()
