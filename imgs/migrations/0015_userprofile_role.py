# Generated by Django 2.0.5 on 2018-10-31 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgs', '0014_auto_20181026_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', '系统管理员'), ('user', '录入人'), ('viewer', '查看人')], default='viewer', max_length=10, verbose_name='角色'),
        ),
    ]
