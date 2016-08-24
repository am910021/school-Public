from django.contrib import admin
from .models import Setting, Menu, Item, ShinyApp, DBGroupName, DBGroupItem, DBGroupUser
# Register your models here.
admin.site.register(Setting)
admin.site.register(Menu)
admin.site.register(Item)
admin.site.register(ShinyApp)
admin.site.register(DBGroupName)
admin.site.register(DBGroupItem)
admin.site.register(DBGroupUser)