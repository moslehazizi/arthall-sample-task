from django.db import models
from accounts.models import CustomUser

CHOICES = (
    (1, 'poor'),
    (2, 'below average'),
    (3, 'average'),
    (4, 'above average'),
    (5, 'good'),
    (6, 'great'),
)

class ActivityType(models.Model):
    name = models.CharField(max_length=75)
    need_to_aprove = models.BooleanField(default=True)

    def __str__(self):
        if self.need_to_aprove == True:
            aproved = 'بله'
        else:
            aproved = 'خیر'
        return f'{self.name} - نیاز به تایید مدیر: {aproved}'
    
class ActivityStatus(models.Model):
    status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.status
    
class Activity(models.Model):
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='activity_owner',
    )
    activity_title = models.ForeignKey(
        ActivityType,
        on_delete=models.CASCADE,
        related_name='activity_type',
    )
    value = models.IntegerField(choices=CHOICES)
    start_time =models.DateField()
    end_time = models.DateField()
    status = models.ForeignKey(
        ActivityStatus,
        null=True,
        on_delete=models.SET_NULL,
        related_name='activity_status',
    )
    photos = models.ImageField(upload_to='photos/', blank=True)
    desc = models.TextField()
    aproved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.activity_title.name} -- {self.owner} -- from {self.start_time} to {self.end_time} -- {self.status} -- value: {self.value}'



