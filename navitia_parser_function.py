# -*- coding: utf -*-
import json


def get_lines_details():  # parsing lines.txt to get geometry id associated with line id
    line2geometry = []
    index_lines = 0
    with open('../ntfs/lines.txt', 'r') as file:
        for line in file:
            if index_lines > 0:  # skip first line header
                field = line.split(',')
                line_id = field[0]
                geometry_id = field[12]
                if geometry_id != '':
                    line2geometry.append({
                        'line_id': line_id,
                        'geometry_id': geometry_id,
                        'lineColor': '#' + field[7],
                        'lineTextColor': '#' + field[8]
                    })
            index_lines += 1
    # parsing routes.txt to add text color and line color
    with open('../ntfs/routes.txt', 'r') as file:
        index_routes = 0
        for line in file:
            if index_routes > 0:  # skip first line header
                field = line.split(',')
                line_id = field[3]
                geometry_id = field[4]
                if geometry_id != '':
                    line2geometry.append({
                        'line_id': line_id,
                        'geometry_id': geometry_id,
                        'lineColor': '',
                        'lineTextColor': ''
                    })
            index_routes += 1
    return line2geometry


def convert_linestring2float(linestring):  # convert an array of string coordinates to float
    float_linestring = []
    for strCoordinate in linestring:
        lat = float(strCoordinate[0])
        lng = float(strCoordinate[1])
        float_linestring.append([lat, lng])
    return float_linestring


def write2file(geojson_items, index, former_index):  # write data to a file and increment name
    geojson_collection = {
        "type": "FeatureCollection",
        "features": geojson_items
    }
    name = '../geojson/data_' + str(former_index) + '-' + str(index) + '.json'
    with open(name, 'w') as output_file:
        json.dump(geojson_collection, output_file)
    print("\tData saved inside :", name)
