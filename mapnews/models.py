from djgeojson.fields import PointField
from django.db import models


class MapnewsHotspot(models.Model):

    title = models.CharField(max_length=256)
    description = models.TextField(max_length=3000)
    # picture = models.ImageField()
    dia = models.IntegerField(null=True)
    geom = PointField()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return 'News: {}'.format(self.title)

        # @property
    # def picture_url(self):
    #     return self.picture.url
