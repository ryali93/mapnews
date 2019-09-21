# from djgeojson.fields import PolygonField
from django.db import models
from django.contrib.gis.db import models as geomodels


class NewsHotspot(models.Model):

    title = models.CharField(max_length=256)
    description = models.TextField()
    picture = models.ImageField()
    # geom = PolygonField()
    geom = geomodels.PointField()

    def __unicode__(self):
        return self.title

    @property
    def picture_url(self):
        return self.picture.url
