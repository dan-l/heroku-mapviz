from django.core.management.base import BaseCommand, CommandError
from pprint import pprint
from .GeoUtils import GeoUtils
from sets import Set

# Models
from polls.models import Incident, Coordinate, Institution, Zone, Score


class Command(BaseCommand):
    help = 'Calculate score Table'

    def handle(self, *args, **options):
      Score.objects.all().delete()
      scores = self.get_scores()

    '''
    For each zone, calculate the score, for each year, based on
    1) distance of zone to each institution
    2) crashes in the zone
    '''
    def get_scores(self):
      zones = Zone.objects.all()
      years = self.get_years()
      scores = []
      for zone in zones:
          zone_name = zone.name
          zone_coord = (zone.center_lat, zone.center_lon)
          institution_score = self.get_zone_inst_score(zone_coord)
          years_to_crash_score = self.get_zone_crash_score(zone_name, years)
          for year, crash_score in years_to_crash_score.iteritems():
            total_score = crash_score + institution_score
            score = Score(name=zone_name, raw_score=total_score, year=year)
            scores.append(score)
      scale_scores = self.scale_scores(scores)
      for s in scale_scores:
        pprint(s)
        s.save()

    '''
    Score is scaled to 1-5, higher score is better
    '''
    def scale_scores(self, scores):
      scale_min = 1
      scale_max = 5
      raw_scores = map(lambda s: s.raw_score,scores)
      score_min = min(raw_scores)
      score_max = max(raw_scores)
      for s in scores:
        raw_score = s.raw_score
        # newvalue = a * value + b. a = (max'-min')/(max-min) and b = max' - a * max
        a = (scale_max - scale_min)/(score_max - score_min)
        b = scale_max - a * score_max
        score_scaled = a * raw_score + b
        s.score = round(score_scaled)
      return scores

    def get_years(self):
      years = Set()
      incidents = Incident.objects.all()
      for inc in incidents:
        years.add(inc.year)
      return years

    def get_inst_weights(self):
      weights = dict()
      weights['Sports Fields'] = 0.6
      weights['Hospital'] = 0.8
      weights['Police'] = 0.7
      weights['School Public'] = 0.5
      return weights

    def get_zone_inst_score(self, zone_coord):
      inst_weight = self.get_inst_weights();
      institution_score = 0
      institutions = Institution.objects.all()
      for ins in institutions:
          # score = weight * distance
          # weight is base on the type of institution
          inst_coord = (ins.lat, ins.lon)
          distance = GeoUtils().distance(zone_coord, inst_coord)
          institution_score += inst_weight[ins.institution_type] * distance
      return institution_score

    def get_zone_crash_score(self, zone_name, years):
      years_to_crash_score = dict()
      years_to_crash_count = self.get_year_to_crash_count(zone_name)
      for year in years:
        # score = weight * crash_score
        crash_weight =  0.9
        if year in years_to_crash_count:
          crash_score = crash_weight * years_to_crash_count[year]
        else:
          crash_score = crash_weight
        years_to_crash_score[year] = crash_score
      return years_to_crash_score

    def get_year_to_crash_count(self, zone_name):
      incidents = Incident.objects.filter(zone_name=zone_name)
      crash_count = dict()
      for inc in incidents:
          current_year = inc.year
          current_count = 1 - inc.norm_count
          if current_year in crash_count:
              crash_count[current_year] *= current_count
          else:
              crash_count[current_year] = current_count
      return crash_count
