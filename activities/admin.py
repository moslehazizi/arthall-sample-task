from django.contrib import admin
from .models import ActivityType, ActivityStatus, Activity

'''
register all 3 model to django admin site, So superuser can manage all models.
'''

admin.site.register(ActivityType)
admin.site.register(ActivityStatus)
admin.site.register(Activity)
