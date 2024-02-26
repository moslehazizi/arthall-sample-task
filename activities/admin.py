from django.contrib import admin
from .models import ActivityType, ActivityStatus, Activity


admin.site.register(ActivityType)
admin.site.register(ActivityStatus)
admin.site.register(Activity)
