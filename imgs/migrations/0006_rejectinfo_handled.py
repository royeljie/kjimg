# Generated by Django 2.0.5 on 2018-05-22 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgs', '0005_auto_20180522_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='rejectinfo',
            name='handled',
            field=models.BooleanField(default=False, verbose_name='是否已处理'),
        ),
    ]
