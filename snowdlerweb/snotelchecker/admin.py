from django.contrib import admin

from .models import Site

class SiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Site, SiteAdmin)
