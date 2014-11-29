"""Example to retrieve image from wms server by using owslib and direct method.
"""

__author__ = 'ismailsunni'
__project_name = 'OWS Get Map'
__filename = 'ows_get_map'
__date__ = '07/11/14'
__copyright__ = 'imajimatika@gmail.com'
__doc__ = ''

from owslib.wms import WebMapService
import random
from datetime import datetime
import os
import webbrowser
import urllib


def save_image(filename, image):
    """Save image to filename."""
    if not image:
        print 'Image is probably None'
        return
    out = open(filename, 'wb')
    out.write(image.read())
    out.close()
    if os.path.exists(filename):
        print 'Success, saved in %s' % filename
    else:
        print 'Failed to save in %s' % filename

def construct_url(uri, bbox, srs, size, image_format, styles, layers):
    """Constructing URL for retrieving image from WMS Server."""
    full_uri = uri
    full_uri += '&BBOX=%s' % ",".join(map(str, bbox))
    full_uri += '&SRS=%s' % srs
    full_uri += '&HEIGHT=%d&WIDTH=%d' % size
    full_uri += '&TRANSPARENT=true'
    full_uri += '&FORMAT=%s' % image_format
    full_uri += '&STYLES=%s' % ",".join(map(str, styles))
    full_uri += '&LAYERS=%s' % ','.join(layers)
    full_uri += '&VERSION=1.1.1'
    full_uri += '&REQUEST=GetMap'
    full_uri += '&SERVICE=WMS'

    return full_uri

def retrieve_map_owslib(uri, bbox, srs, size, image_format, styles, layers, wms=None):
    """Retrieve image of a map from wms server using owslib."""
    
    print 'Use owslib method'
    if not wms:
        # Get the wms object
        wms = WebMapService(uri)

    # This is important to make sure they have the same length
    if len(styles) != len(layers):
        styles = [''] * len(layers)

    image = wms.getmap(
        layers=layers,
        styles=styles,
        srs=srs,
        bbox=bbox,
        size=size,
        format=image_format,
        transparent=True
    )

    return image

def retrieve_map_direct(uri, bbox, srs, size, image_format, styles, layers):
    """Retrieve image of a map from wms server using direct get map request."""
    print 'Use direct method'
    full_uri = construct_url(uri, bbox, srs, size, image_format, styles, layers)   
    image = urllib.urlopen(full_uri)

    return image

def get_full_map(uri, base_name=None, layers=None, size=(300,300)):
    print 'Get map for %s' % uri

    # Get the wms object
    wms = WebMapService(uri)

    # Get random layer if not specified
    if not layers:
        layers = list(wms.contents)
    # Set to maximum 5 layers
    if len(layers) > 5:
        layers = random.sample(layers, 5)

    print 'layers', layers
    
    # Set crs
    srs='EPSG:4326'
    
    # Get bounding box of the layers
    bbox = wms.contents[layers[0]].boundingBoxWGS84
    print 'bbox', bbox
    
    # Get image formats
    image_formats = wms.getOperationByName('GetMap').formatOptions
    
    if 'image/png' in image_formats:
        image_format = 'image/png'
    elif 'image/jpeg' in image_formats:
        image_format = 'image/jpeg'
    else:
        image_format = image_formats[0]
    print 'image_format', image_format

    styles = []

    image = None

    try:
        image = retrieve_map_owslib(uri, bbox, srs, size, image_format, styles, layers, wms)
    except Exception, e:
        print 'Can not use retrieve_map_owslib because %s' % e

    if not image:
        try:
            image = retrieve_map_direct(uri, bbox, srs, size, image_format, styles, layers)
        except Exception, e:
            print 'Can not use retrieve_map_direct because %s' % e

    if not image:
        print 'Failed to download'
        return

    # Generate filename
    if not base_name:
        base_name = 'map'
    now = datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    extension = image_format.split('/')[1]
    filename = '%s_%s.%s' %  (base_name, now_str, extension)

    # Save image
    save_image(filename, image)

def main():
    wms = {
        # No longer active
        # 'wms_boston_freemaps' : 'http://boston.freemap.in/cgi-bin/mapserv',
        # 'wms_cia_world_factbook' : 'http://world.freemap.in/cgi-bin/mapserv?map=/www/freemap.in/world/map/factbook.map',
        # 'wms_topomaps' : 'http://terraservice.net/ogcmap.ashx',
        # 'wms_shaded_relief' : 'http://ims.cr.usgs.gov/servlet19/com.esri.wms.Esrimap/USGS_EDC_Elev_NED_3',
        # 'wms_nexrad' : 'http://online.resource.url/wms/script'
        # 'wms_lab_metacarta' : 'http://labs.metacarta.com/wms/vmap0',
        # 'wms_nasa' : 'http://wms.jpl.nasa.gov/wms.cgi',
        # 'wms_pop_density' : 'http://beta.sedac.ciesin.columbia.edu/mapserver/wms/gpw2000',
        # 'wms_human_footprint' : 'http://beta.sedac.ciesin.columbia.edu/mapserver/wms/hfoot',
        # 'wms_NYC_freemap' : 'http://nyc.freemap.in/cgi-bin/mapserv?MAP=/www/freemap.in/nyc/map/basemap.map',
        
        # Still active until my last commit
        'wms_kartoza' : 'http://maps.kartoza.com/cgi-bin/qgis_mapserv.fcgi?map=/web/Boosmansbos/Boosmansbos.qgs',
        'wms_massgis' : 'http://giswebservices.massgis.state.ma.us/geoserver/wms',
        'wms_dm_solutions' : 'http://www2.dmsolutions.ca/cgi-bin/mswms_gmap',
        'wms_USGS_topo' : 'http://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer'
    }

    for name, uri in wms.iteritems():
        try:
            get_full_map(uri, name)
        except Exception, e:
            print 'Failed:', e
        finally:
            print 


if __name__ == '__main__':
    main()