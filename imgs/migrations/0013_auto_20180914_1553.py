# Generated by Django 2.0.5 on 2018-09-14 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imgs', '0012_auto_20180604_1740'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='param',
            options={'ordering': ['code'], 'verbose_name': '系统参数', 'verbose_name_plural': '系统参数'},
        ),
        migrations.AlterModelOptions(
            name='rejectinfo',
            options={'ordering': ['time'], 'verbose_name': '退回信息', 'verbose_name_plural': '退回信息'},
        ),
    ]
