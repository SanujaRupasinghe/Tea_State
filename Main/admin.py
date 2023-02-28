from django.contrib import admin
from .models import *

admin.site.register(Entry)
admin.site.register(Employee)
admin.site.register(Work)
admin.site.register(Section)

admin.site.register(Employee_Work)
admin.site.register(Section_Work)


