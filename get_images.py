#!/usr/bin/env python
"""A script to download all images in a web page."""

__author__ = 'Ismail Sunni'
__copyright__ = 'Ismail Sunni'
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Ismail Sunni'
__email__ = 'imajimatika@gmail.com'
__status__ = 'Prototype'
__date__ = '29 Nov 2013'

import urllib
import urllib2
import os
from BeautifulSoup import BeautifulSoup


def get_page_soup(url):
    """Download a page and return a BeautifulSoup object of the html"""
    response = urllib2.urlopen(url)
    html = response.read()
    return BeautifulSoup(html)

def get_image_links(url):
    """Get all image links from a url."""
    image_links = []
    page_soup = get_page_soup(url)
    image_elements = page_soup.findAll('img')
    for image_element in image_elements:
        image_link = image_element.get('src')
        image_links.append(image_link)

    return image_links

def download_file(file_url, parent_directory='', file_name=None):
    """Download file to parent_directory as file_name."""
    if not file_name:
        file_name = file_url.split('/')[-1]
    if not os.path.exists(parent_directory):
        os.mkdir(parent_directory)

    local_path = os.path.join(parent_directory, file_name)
    urllib.urlretrieve(file_url, local_path)

    if os.path.exists(local_path):
        return local_path
    else:
        return None

def get_all_images(url, parent_directory=''):
    """Download all images from a web page (url) to parent_directory."""
    image_links = get_image_links(url)
    succes = 0
    failed = 0
    for image_link in image_links:
        print 'Try to download %s' % image_link
        try:
            local_path = download_file(image_link, parent_directory)
            if os.path.exists(local_path):
                print 'Succes to download %s, saved to %s' % (
                    image_link, local_path)
                succes += 1
            else:
                print 'Failed to download %s' % image_link
                failed += 1
        except Exception, e:
            print 'Failed to download %s' % image_link
            failed += 1
    print 'Number of successful download %d' % succes
    print 'Number of failed download %d' % failed
    print 'Total image links available %d' % len(image_links)
        

if __name__ == '__main__':
    get_all_images('http://www.aliexpress.com/snapshot/6263822273.html', 'alibaba_sjcam')