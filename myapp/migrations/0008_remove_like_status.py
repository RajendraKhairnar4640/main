# Generated by Django 4.1.1 on 2022-10-11 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_like_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='status',
        ),
    ]
