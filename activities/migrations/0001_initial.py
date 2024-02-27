# Generated by Django 4.0.10 on 2024-02-27 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('need_to_aprove', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'poor'), (2, 'below average'), (3, 'average'), (4, 'above average'), (5, 'good'), (6, 'great')])),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('photos', models.ImageField(blank=True, upload_to='photos/')),
                ('desc', models.TextField()),
                ('aproved', models.BooleanField(default=False)),
                ('activity_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_type', to='activities.activitytype')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_owner', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_status', to='activities.activitystatus')),
            ],
        ),
    ]
