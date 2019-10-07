import json

def getGeometryIdwithLineId():
    lineId2geometryId = []
    indexLines = 0
    with open('../ntfs/lines.txt', 'r') as file:
        for line in file:
            if indexLines > 0:  # skip first line header
                field = line.split(',')
                lineId = field[0]
                geometryId = field[12]
                if geometryId != '':
                    lineId2geometryId.append({
                        'lineId': lineId,
                        'geometryId': geometryId,
                        'lineColor': '#' + field[7],
                        'lineTextColor': '#' + field[8]
                    })
            indexLines += 1

    with open('../ntfs/routes.txt', 'r') as file:
        indexRoutes = 0
        for line in file:
            if indexRoutes > 0:  # skip first line header
                field = line.split(',')
                lineId = field[3]
                geometryId = field[4]
                if geometryId != '':
                    lineId2geometryId.append({
                        'lineId': lineId,
                        'geometryId': geometryId,
                        'lineColor': '',
                        'lineTextColor': ''
                    })
            indexRoutes += 1
    return lineId2geometryId

def strLineString2Float(strLineString):
    floatLineString = []
    for strCoordinate in strLineString:
        lat = float(strCoordinate[0])
        lng = float(strCoordinate[1])
        floatLineString.append([lat, lng])
    return floatLineString

def write2file(arrayOfGeojsonItems, index, formerIndex):
    geojsonCollection = {
        "type": "FeatureCollection",
        "features": arrayOfGeojsonItems
    }
    name = '../geojson/data_' + str(formerIndex) + '-' + str(index) + '.json'
    with open(name, 'w') as output_file:
        json.dump(geojsonCollection, output_file)
    print("\tData saved inside :", name)