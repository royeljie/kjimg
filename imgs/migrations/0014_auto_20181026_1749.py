# Generated by Django 2.0.5 on 2018-10-26 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imgs', '0013_auto_20180914_1553'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='accountCode',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='accountDetail',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='accountName',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='amount',
        ),
    ]
