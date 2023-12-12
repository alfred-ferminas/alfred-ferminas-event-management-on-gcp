from django.contrib import admin

from .models import *

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(usermails)
admin.site.register(registeredevents)
admin.site.register(notification)
admin.site.register(registration)