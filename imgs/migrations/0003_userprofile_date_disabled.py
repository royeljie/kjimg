# Generated by Django 2.0.5 on 2018-05-10 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgs', '0002_auto_20180510_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_disabled',
            field=models.DateTimeField(null=True, verbose_name='停用时间'),
        ),
    ]
