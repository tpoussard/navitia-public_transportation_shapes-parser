import json
from navitia_parser_function import *

arrayOfGeojsonItems=[]
index = 0
formerIndex = 0
properties = {}
notFoundIndex = 0

# parse files lines.txt and routes.txt to associate a geometry_id with a lineId
geometry2line_id = get_lines_details()
# open file geometries.txt, read and format coordinates in JSON format
with open('../ntfs/geometries.txt', 'r') as file:
    for line in file:
        if index > 0:
            field = line.split(',', 1)
            geometry_id = field[0]
            print('geometry_id', geometry_id)
            properties = {'geometry_id': geometry_id}

    # search for routeId matching geometry_id to fill properties
            # test to factorize:
            # properties = [obj for obj in geometry2line_id if obj['geometry_id'] == geometry_id]
            for obj in geometry2line_id:
                if obj['geometry_id'] == geometry_id:
                    properties.update({
                        'line_id': obj['line_id'],
                        'lineColor': obj['lineColor'],
                        'lineTextColor': obj['lineTextColor']
                    })
                    break

            if 'line_id' not in properties:  # check if lineId is missing
                print('no corresponding lineId found for geometry_id:', geometry_id, properties)
            if properties['line_id'] == '':  # check if lineID is empty
                notFoundIndex += 1
        #  format shape data from CSV format to json format
            #  remove parenthesis
            rawMultiLine = field[1].split('((')[-1]  # at the beginning
            rawMultiLine = rawMultiLine.split('))"') # at the end
            rawMultiLine = rawMultiLine[0].split('),(')  # between shape segments
            #  create an array of arrays
            coordinates = []
            for rawLineString in rawMultiLine:
                str_linestring = rawLineString.split(',')
                coordinates.append(convert_linestring2float([strCoordinates.split(' ') for strCoordinates in str_linestring]))

    # Format object
            arrayOfGeojsonItems.append({
                        "type": "Feature",
                        "properties": properties,
                        "geometry": {
                            "type": "MultiLineString",
                            "coordinates": coordinates
                        }
                    })
            if len(properties) == 0:  # check if properties is missing
                print('missing properties for geometry_id', geometry_id)
    # split and save when reaching 110 public transportation line object to avoid big files
        # in order to be able to add them manually to mapbox for instance
            if index % 110 == 0:
                write2file(arrayOfGeojsonItems, index, formerIndex)

                formerIndex = index + 1
                if notFoundIndex != 0:  # check if there was missing shape
                    print('\nMissing lineIds =', notFoundIndex)
                arrayOfGeojsonItems = []
                notFoundIndex = 0
        index += 1
    #  save the rest of shapes at the end
    write2file(arrayOfGeojsonItems, index, formerIndex)
