# Generated by Django 5.0.6 on 2024-07-01 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackerRank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissions',
            name='duringContest',
        ),
    ]
