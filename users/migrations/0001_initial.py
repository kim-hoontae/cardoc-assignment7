# Generated by Django 3.2.9 on 2021-11-26 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
