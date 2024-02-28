from django.db import models
from accounts.models import CustomUser

'''
در این فایل مدل مناسب برای ثبت فعالیت برای هنرمندان تعریف شده است. 
مدل تعریف شده برای ثبت فعالیت است که دارای 9 فیلد است  'Activity' مدل

1- owner: دارد. یعنی هر کاربر میتواند چندین فعالیت ثبت شده داشته باشد OneToMany این فیلد برای ارایه نام هنرمدی است که فعالیت را انجام داده است که با مدل کاربرها ارتباط 
2- activity_title:  ActivityType این فیلد عنوان یا نوع فعالیت را مشخص می کند که انتخاب آن از طریق مدلی دیگری است به نام
        - ActivityType model: 
            این مدل ایجاد شده است تا هنرمند بتواند از میان فعالیت های استاندارد موجود
            که در فایل راهنمای تسک آمده است. نوع فعالیت خود را انتخاب کند یا ادمین بتوان فعالیتی
             با آن عنوان را به نام او ثبت کند. این مدل دارای دو فیلد 'نام' و 'نیاز به تایید مدیر' است 
            زیرا تعدادی از فعالیت ها برای ثبت نیاز به تایید مدیر ندارند یعنی هنرمند می تواند
            تعدادی از فعالیت هایی را که ثبت می کند بدون تایید مدیر در پروفایل خود ببیند.
3- value: ایجاد شده اند. انتخاب می کنند CHOICES این فیلد برای ارزش گذاری فعالیت تعریف شده است. هنرمند یا ادمین برای ارزش گذاری فعالیت از میان انتخاب هایی که در 
4- start_time: تاریخ شروع فعالیت
5- end_time: تاریخ پایان فعالیت
6- status: برای انتخاب یکی از این وضعیت ها استفاده میکند ActivityStatus این فیلد وضعیت فعالیت را نشان میدهد(در حال انجام یا تکمیل شده) که از مدل   
7- photos: گالری تصاویر فعالیت
8- desc: توضیحات فعالیت
9- aproved: این فیلد وضعیت فعالیت (تایید شده توسط ادمین یا خیر) را نشان می دهد.
             اگر فعالیت از نوعی باشد که نیاز به تایید مدیر نداشته باشد تایید یا عدم تایید این فیلد تاثیری در وضعیت نمایش آن فعالیت ندارد. 

'''     

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



