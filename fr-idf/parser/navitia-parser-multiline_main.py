import json
from tasks_parser_multiline_string_function import *

geometryNlineIds_colored = getGeometryIdwithLineId()
arrayOfGeojsonItems=[]
index = 0
formerIndex = 0
properties = {}
notFoundIndex = 0
with open('../ntfs/geometries.txt', 'r') as file:
    for line in file:
        if index > 0:
            field = line.split(',', 1)
            geometryId = field[0]
            print('geometryId', geometryId)
            properties = {'geometryId': geometryId}
    # search for routeId matching geometryId to fill properties
            # properties = [obj for obj in geometryNlineIds_colored if obj['geometryId'] == geometryId]
            for obj in geometryNlineIds_colored:
                if obj['geometryId'] == geometryId:
                    properties.update({'lineId': obj['lineId'], 'lineColor': obj['lineColor'], 'lineTextColor': obj['lineTextColor']})
                    break
            if not 'lineId' in properties:
                print('no corresponding geometryId found for geometryId:', geometryId, properties)
            if properties['lineId'] == '':
                notFoundIndex += 1
            rawMultiLine = field[1].split('((')[-1]
            rawMultiLine = rawMultiLine.split('))"')
            rawMultiLine = rawMultiLine[0].split('),(')
            coordinates = []
            for rawLineString in rawMultiLine:
                strLineString = rawLineString.split(',')
                coordinates.append(strLineString2Float([strCoordinates.split(' ') for strCoordinates in strLineString]))

# Formating object and saving
            geojsonFeature = {
                        "type": "Feature",
                        "properties": properties,
                        "geometry": {
                            "type": "MultiLineString",
                            "coordinates": coordinates
                        }
                    }
            arrayOfGeojsonItems.append(geojsonFeature)
            if len(properties) == 0:
                print('missing properties for geometryId', geometryId)
            if index % 110 == 0:
                write2file(arrayOfGeojsonItems, index, formerIndex)
                formerIndex = index + 1
                if notFoundIndex != 0:
                    print('\nMissing lineIds =', notFoundIndex)
                arrayOfGeojsonItems = []
                notFoundIndex = 0
        index += 1
    write2file(arrayOfGeojsonItems, index, formerIndex)