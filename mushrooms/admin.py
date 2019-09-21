from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from . import models as newshotspot_models


admin.site.register(newshotspot_models.NewsHotspot, LeafletGeoAdmin)
