import pickle

from django.core.management.base import BaseCommand, CommandError
import csv
from os import path, pardir
import polls
from .GeoUtils import GeoUtils
from pprint import pprint
import polls

# Raw Data Path names
POLLS = polls.__path__[0]
RAW_DATA_PATH = path.join(POLLS, 'raw_data')
POLICE = path.join(RAW_DATA_PATH, 'POLICE.csv')
HOSPITALS = path.join(RAW_DATA_PATH, 'HOSPITALS.csv')
SCHOOLS = path.join(RAW_DATA_PATH, 'SCHOOLS.csv')
FIELDS = path.join(RAW_DATA_PATH, 'FIELDS.csv')
ZONE_NAME_TO_POLYGON_PATH = \
    path.join(path.abspath(path.join(polls.__path__[0], pardir)), 'temp.py')

# Models
from polls.models import Institution

class Command(BaseCommand):
    help = 'Load initial institution data into Institution Table'
    with open(ZONE_NAME_TO_POLYGON_PATH, 'r') as read_file:
        zone_name_to_polygon_dict = pickle.load(read_file)

    def parseInstitutions(self, filename, quotechar, name_index, lat_index, lon_index, type_index):
         with open(filename, 'rb') as csvfile:
            # replace null byte
            reader = csv.reader((x.replace('\0', '') for x in csvfile), delimiter=',', quotechar=quotechar)
            # skip header
            next(reader)
            for idx, row in enumerate(reader):
                ins = Institution()
                ins.name = row[name_index]
                ins.lon = float(row[lat_index])
                ins.lat = float(row[lon_index])
                ins.institution_type = row[type_index]

                matched_zone = GeoUtils().isIncidentInPolygon((ins.lat, ins.lon), self.zone_name_to_polygon_dict)
                if (matched_zone != None):
                    ins.zone_name = matched_zone
                    pprint(ins)
                    ins.save()

                self.stdout.write("Successfully Load Institution Model")


    def handle(self, *args, **options):
        Institution.objects.all().delete()
        self.parseInstitutions(POLICE, None, 0, 33, 34, 0)
        self.parseInstitutions(HOSPITALS, '"', 0, 33, 34, 0)
        self.parseInstitutions(SCHOOLS, '"', 0, 33, 34, 0)
        self.parseInstitutions(FIELDS, '"', 2, 0, 1, 2)