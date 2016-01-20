# coding=utf-8
"""Changing raster layer transparency via python in QGIS.

author: Ismail Sunni (imajimatika@gmail.com)
created: 18 January 2016
"""

from qgis.core import QgsRasterTransparency

print 'Start'

transparency = QgsRasterTransparency.TransparentSingleValuePixel()
transparencies = []
transparency.min = 0
transparency.max = 0
transparency.percentTransparent = 50
transparencies.append(transparency)

active_layer = qgis.utils.iface.mapCanvas().currentLayer()
active_layer.renderer().rasterTransparency().setTransparentSingleValuePixelList(transparencies)
active_layer.triggerRepaint()

print 'Finish'
