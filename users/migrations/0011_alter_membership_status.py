# Generated by Django 5.1.6 on 2025-03-18 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_membership_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Expired', 'Expired')], default='Active', max_length=10),
        ),
    ]
