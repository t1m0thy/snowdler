from django.db import models

# Create your models here.

class Site(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    code = models.CharField(max_length=12)
    selected = models.BooleanField(default=False)
    county = models.CharField(max_length=255)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    def __str__(self):
        return "{}, {} County, {}".format(self.name, self.county, self.state)

