from django.core.management.base import BaseCommand, CommandError
import json
from os import path
from os import listdir
import polls
from pprint import pprint

# Raw Data Path names
POLLS = polls.__path__[0]
ZONES = path.join(POLLS, 'raw_data', 'zones')

# Models
from polls.models import Coordinate
from polls.models import Zone
from GeoUtils import *

class Command(BaseCommand):
    help = 'Load initial Coordinate data into Coordinate Table'

    def get_data_absolute_paths(self):
        result = []
        zones_sub_paths = listdir(ZONES)
        for sub_path in zones_sub_paths:
            current_path = path.join(ZONES, sub_path)
            result.append(current_path)
        return result

    def handle(self, *args, **options):
        data_paths = self.get_data_absolute_paths()
        Zone.objects.all().delete()
        Coordinate.objects.all().delete()
        for path in data_paths:
            try:
                with open(path, 'r') as json_file:
                    current = json.load(json_file)
                    features = self.getFeaturesList(current)
                    if (features == None):
                        self.stderr.write("Missing Features")
                        return

                    for f in features:
                        self.load_coordinate_row(f)
            except IOError as err:
                print("Unable to open file " + str(err))

        self.stdout.write('Successfully Loaded Initial Coordinate Data')

    def getID(self, feature):
        if ("id" not in feature or
                    feature["id"] == None):
            return None
        return feature["id"]

    def getLocationList(self, feature):
        if ("geometry" not in feature or
                    feature["geometry"] == None):
            pprint("Missing geometry")
            return None
        geometry = feature["geometry"]
        if ("coordinates" not in geometry or
                    geometry["coordinates"] == None):
            pprint("Missing coordinates")
            return None
        # map it from 3-point coordinates into 2-point coordinates
        return map((lambda x: (x[0], x[1])),geometry["coordinates"][0]);

    def getFeaturesList(self, data):
        if ("features" not in data or
                    data["features"] == None):
            return None
        return data["features"]

    def load_coordinate_row(self, feature):
        id = self.getID(feature)
        locations = self.getLocationList(feature)

        if (feature == None or id == None):
            self.stderr.write("missing id or locations")
            return

        # For current zone, load coordinates
        zone = Zone()
        zone.name = feature["id"]
        zone.zone_type = feature["properties"]["Name"]
        zone_center = GeoUtils().getCentroid(locations)
        zone.center_lat = zone_center[1]
        zone.center_lon = zone_center[0]
        zone.save()
        print("**** created zone:", zone)

        for lat_lon in locations:
            lat = lat_lon[0]
            lon = lat_lon[1]
            coordinate = \
                Coordinate(name=zone, lat=lat, lon=lon)
            coordinate.save()
            print("added", coordinate)
