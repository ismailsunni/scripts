# Love equation: x^{2}+\left(y-\sqrt{\left|x\right|}\right)^{2}=1
# Positive love: y=\sqrt{\left(1-x^{2}\right)}\ +\ \sqrt{\left|x\right|}
# Negative love: y=-\sqrt{\left(1-x^{2}\right)}\ +\ \sqrt{\left|x\right|}
# Reference: https://www.desmos.com/calculator/9vwjltfkwg

import math
import numpy as np
from osgeo import ogr

def love_positive(x):
    return math.sqrt(1 - x*x) + math.sqrt(abs(x))

def love_negative(x):
    return -math.sqrt(1 - x*x) + math.sqrt(abs(x))

love_points = []
positive_points = []
negative_points = []

number_of_points = 101

for i in np.linspace(-1, 1, number_of_points):
    positive_points.append((i, love_positive(i)))

for i in np.linspace(1, -1, number_of_points):
    negative_points.append((i, love_negative(i)))

love_points = positive_points + negative_points

for p in love_points:
    print(p)

ring = ogr.Geometry(ogr.wkbLinearRing)

for p in love_points:
    ring.AddPoint(p[0], p[1])

love_poly = ogr.Geometry(ogr.wkbPolygon)
love_poly.AddGeometry(ring)

print(love_poly.ExportToWkt())


# Create the output Driver
outDriver = ogr.GetDriverByName('GeoJSON')

# Create the output GeoJSON
outDataSource = outDriver.CreateDataSource('love.geojson')
outLayer = outDataSource.CreateLayer('love.geojson', geom_type=ogr.wkbPolygon )

# Get the output Layer's Feature Definition
featureDefn = outLayer.GetLayerDefn()

# create a new feature
outFeature = ogr.Feature(featureDefn)

# Set new geometry
outFeature.SetGeometry(love_poly)

# Add new feature to output Layer
outLayer.CreateFeature(outFeature)

# dereference the feature
outFeature = None

# Save and close DataSources
outDataSource = None