from qgis.core import QgsRasterTransparency

print 'Start'
active_layer = l = qgis.utils.iface.mapCanvas().currentLayer()
raster_transpareny  = active_layer.renderer().rasterTransparency()
ltr = QgsRasterTransparency.TransparentSingleValuePixel()
tr_list = []
ltr.min = 0
ltr.max = 0
ltr.percentTransparent = 50
tr_list.append(ltr)
active_layer.renderer().rasterTransparency().setTransparentSingleValuePixelList(tr_list)

active_layer.triggerRepaint()
print 'Finish'