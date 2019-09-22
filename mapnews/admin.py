from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from . import models as mapnews_models


admin.site.register(mapnews_models.MapnewsHotspot, LeafletGeoAdmin)
