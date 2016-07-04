from django.contrib import admin
from .models import SchoolData , Department, Work
# Register your models here.

admin.site.register(SchoolData)
admin.site.register(Department)
admin.site.register(Work)