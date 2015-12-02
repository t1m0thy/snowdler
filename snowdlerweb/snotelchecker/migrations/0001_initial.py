# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=2)),
                ('code', models.CharField(max_length=12)),
                ('selected', models.BooleanField(default=False)),
                ('county', models.CharField(max_length=255)),
                ('lat', models.FloatField(null=True)),
                ('lon', models.FloatField(null=True)),
            ],
        ),
    ]
