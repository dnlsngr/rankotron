from django.db import models

# Create your models here.

class League(models.Model):
    league_name = models.CharField(max_length=200)
    league_id   = models.CharField(max_length=32)
    last_fetched= models.DateTimeField()

class Team(models.Model):
    team_name   = models.CharField(max_length=200)
    team_id     = models.CharField(max_length=32)
    league      = models.ForeignKey(League)

class Week(models.Model):
    week_number = models.IntegerField(blank=True)
    team        = models.ForeignKey(Team)

class Position(models.Model):
    pos_name    = models.CharField(max_length=8)
    points      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    week        = models.ForeignKey(Week)


