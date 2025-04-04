# Generated by Django 5.1.6 on 2025-03-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_activity_alter_booking_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='location',
        ),
        migrations.AlterField(
            model_name='activity',
            name='availability_status',
            field=models.BooleanField(default=True, help_text='Check if the activity is available'),
        ),
    ]
