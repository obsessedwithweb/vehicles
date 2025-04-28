from django import forms
from django.contrib import admin
from .models import Vehicle, Advertises, Blog, Services, models


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 60})},
    }


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['title']

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 60})},
    }

admin.site.register(Advertises)

