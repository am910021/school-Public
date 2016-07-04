from django.contrib import admin
from .models import Setting, Menu, Item, ShinyApp, DBItemGroupName, DBItemGroups
# Register your models here.
admin.site.register(Setting)
admin.site.register(Menu)
admin.site.register(Item)
admin.site.register(ShinyApp)
admin.site.register(DBItemGroupName)
admin.site.register(DBItemGroups)