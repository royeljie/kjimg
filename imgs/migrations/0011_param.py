# Generated by Django 2.0.5 on 2018-05-30 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgs', '0010_auto_20180530_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Param',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='参数名称')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='参数代码')),
                ('val', models.CharField(max_length=250, verbose_name='参数值')),
            ],
        ),
    ]
