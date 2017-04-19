from django.core.management.base import BaseCommand, CommandError
import csv
from os import path, pardir
import polls
from .GeoUtils import GeoUtils
from pprint import pprint
import pickle

# Raw Data Path names
POLLS = polls.__path__[0]
RAW_DATA_PATH = path.join(POLLS, 'raw_data')
CRASHES = path.join(RAW_DATA_PATH, 'CRASHES.csv')
ZONE_NAME_TO_POLYGON_PATH = \
    path.join(path.abspath(path.join(polls.__path__[0], pardir)), 'temp.py')

# Models
from polls.models import Incident
from polls.models import Coordinate


class Command(BaseCommand):
    help = 'Load initial Incident data into Incident Table'

    def handle(self, *args, **options):
        with open(ZONE_NAME_TO_POLYGON_PATH, 'r') as read_file:
            zone_name_to_polygon_dict = pickle.load(read_file)

        Incident.objects.all().delete()

        incidents = []
        minCount = 1000
        maxCount = 0

        with open(CRASHES, 'rb') as csvfile:
            # Normalize values

            reader = csv.reader((x.replace('\0', '') for x in csvfile), delimiter=',', quotechar='|')
            # skip header
            next(reader)
            for idx, row in enumerate(reader):
                count = int(row[1])
                minCount = min(minCount, count)
                maxCount = max(maxCount, count)
                inc = Incident()
                inc.name = "CRASH"
                inc.count = count
                inc.lon = float(row[6])
                inc.lat = float(row[3])
                inc.year = row[8]

                matched_zone = GeoUtils().isIncidentInPolygon((inc.lat, inc.lon), zone_name_to_polygon_dict)
                if (matched_zone != None):
                    inc.zone_name = matched_zone
                    incidents.append(inc)
            self.stdout.write("Successfully Load Incidental Model")

        print(minCount, maxCount)

        for inc in incidents:
            inc.norm_count = self.normalize(inc.count, minCount, maxCount)
            inc.save()

    def get_zone_name_to_polygon_dict(self):
        coordinate_rows = Coordinate.objects.all()
        zone_name_to_polygon_dict = {}
        for c_row in coordinate_rows:
            key = c_row.name.name
            location = (c_row.lon, c_row.lat)
            if (key in zone_name_to_polygon_dict):
                zone_name_to_polygon_dict[key].append(location)
            else:
                zone_name_to_polygon_dict[key] = list()
                zone_name_to_polygon_dict[key].append(location)
        return zone_name_to_polygon_dict

    def normalize(self, item, min_item, max_item):
        return (item - min_item) / float(max_item - min_item)
