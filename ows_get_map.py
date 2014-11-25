from owslib.wms import WebMapService
import random
from datetime import datetime
import os

def save_image(filename, image):
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


def get_full_map(uri, base_name=None, layers=None):
    print 'Get map for %s' % uri

    # Get the wms object
    wms = WebMapService(uri, version='1.1.1')

    # Get random layer if not specified
    if not layers:
        layers = [random.choice(list(wms.contents))]
    print 'layers', layers
    
    # Set crs
    srs='EPSG:4326'
    
    # Get bounding box of the layers
    bbox = wms.contents[layers[0]].boundingBoxWGS84
    print 'bbox', bbox
    
    # Get image formats
    image_formats = wms.getOperationByName('GetMap').formatOptions
    if 'image/jpeg' in image_formats:
        image_format = 'image/jpeg'
    elif 'image/png' in image_formats:
        image_format = 'image/png'
    else:
        image_format = image_formats[0]
    print 'image_format', image_format

    # Get the image
    image = wms.getmap(
        layers=layers,
        styles=[''],
        srs=srs,
        bbox=bbox,
        size=(300, 300),
        format=image_format,
        transparent=True
    )

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
        'wms_kartoza' : 'http://maps.kartoza.com/cgi-bin/qgis_mapserv.fcgi?map=/web/Boosmansbos/Boosmansbos.qgs&SERVICE=WMS&VERSION=1.1.1',
        # 'wms_massgis' : 'http://giswebservices.massgis.state.ma.us/geoserver/wms',
        # 'wms_lab_metacarta' : 'http://labs.metacarta.com/wms/vmap0',
        # 'wms_nasa' : 'http://wms.jpl.nasa.gov/wms.cgi',
        # 'wms_pop_density' : 'http://beta.sedac.ciesin.columbia.edu/mapserver/wms/gpw2000',
        # 'wms_human_footprint' : 'http://beta.sedac.ciesin.columbia.edu/mapserver/wms/hfoot',
        # 'wms_NYC_freemap' : 'http://nyc.freemap.in/cgi-bin/mapserv?MAP=/www/freemap.in/nyc/map/basemap.map',
        # 'wms_dm_solutions' : 'http://www2.dmsolutions.ca/cgi-bin/mswms_gmap',
        # 'wms_boston_freemaps' : 'http://boston.freemap.in/cgi-bin/mapserv',
        # 'wms_cia_world_factbook' : 'http://world.freemap.in/cgi-bin/mapserv?map=/www/freemap.in/world/map/factbook.map',
        # 'wms_topomaps' : 'http://terraservice.net/ogcmap.ashx',
        # 'wms_shaded_relief' : 'http://ims.cr.usgs.gov/servlet19/com.esri.wms.Esrimap/USGS_EDC_Elev_NED_3',
        # 'wms_nexrad' : 'http://online.resource.url/wms/script'
    }

    for name, uri in wms.iteritems():
        try:
            get_full_map(uri, name)
        except Exception, e:
            print 'Failed:', e
        finally:
            print 
    # uri = 'http://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer'
    # get_full_map(uri)


if __name__ == '__main__':
    main()