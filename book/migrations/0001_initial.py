# Generated by Django 4.0.6 on 2022-07-31 13:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('original_quantity', models.IntegerField()),
                ('description', models.TextField(max_length=500)),
                ('quantity_now', models.IntegerField()),
                ('created_dt', models.DateTimeField(auto_now=True)),
                ('updated_dt', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
