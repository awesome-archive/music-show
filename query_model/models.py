from __future__ import unicode_literals

from django.db import models


class Alltimeranking(models.Model):
    uname = models.TextField(blank=True, null=True)
    uid = models.TextField(blank=True, null=True)
    birthday = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    song = models.TextField(blank=True, null=True)
    singer = models.TextField(blank=True, null=True)
    addedtime = models.TextField(db_column='addedTime', blank=True, null=True)  # Field name made lowercase.

class Lastweekranking(models.Model):
    uname = models.TextField(blank=True, null=True)
    uid = models.TextField(blank=True, null=True)
    birthday = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    song = models.TextField(blank=True, null=True)
    singer = models.TextField(blank=True, null=True)
    addedtime = models.TextField(db_column='addedTime', blank=True, null=True)  # Field name made lowercase.

class Inserttest(models.Model):
	name = models.TextField(blank=True, null=True)
	uid = models.TextField(blank=True, null=True)