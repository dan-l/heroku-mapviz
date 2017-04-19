from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Zone(models.Model):
    name = models.IntegerField(primary_key=True)
    zone_type = models.CharField(max_length=30)
    center_lat = models.FloatField()
    center_lon = models.FloatField()

    def __str__(self):
        return "ZONE " + str(self.name) + " TYPE: " + str(self.zone_type) + " CENTER: (" + str(self.center_lat) + ", " + str(self.center_lon) + ")"

class Coordinate(models.Model):
    name = models.ForeignKey(Zone, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    def __str__(self):
        return str(self.name) + ' at ( lat : ' + str(self.lat)  + ' , lon : ' + str(self.lon) + ') '


class Score(models.Model):
    name = models.IntegerField()
    year = models.IntegerField()
    raw_score = models.FloatField()
    score = models.IntegerField()
    def __str__(self):
        return 'SCORE for zone: ' + str(self.name) + ' year: ' + str(self.year) + ' is ' + str(self.score) + ', raw score: ' + str(self.raw_score)


class Incident(models.Model):
    name = models.CharField(max_length=30)
    lat = models.FloatField()
    lon = models.FloatField()
    year = models.IntegerField()
    count = models.IntegerField()
    norm_count = models.FloatField()
    zone_name = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __unicode__( self ):
        return "INCIDENT: name {0} latlon ({1},{2}), year {3}, count{4}, norm_count{5}, zone_name{6}".format( self.name, self.lat, self.lon, self.year, self.count, self.norm_count, self.zone_name.__str__())


class Institution(models.Model):
    name = models.CharField(max_length=30)
    lat = models.FloatField()
    lon = models.FloatField()
    institution_type = models.CharField(max_length=30)
    zone_name = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + '. type ' + self.institution_type + ' lat ' + str(self.lat) + ' lon ' + str(self.lon) + " is in zone name " + str(self.zone_name.name)




