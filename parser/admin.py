from django.contrib import admin
from .models import Selector

# Register your models here.
@admin.register(Selector)
class SelectorAdmin(admin.ModelAdmin):
    list_display = ('platform', 'search_box', 'search_button', 'next_button', 'item', 'title', 'price', 'link')
    search_fields = ('platform',)