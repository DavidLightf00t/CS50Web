# Generated by Django 5.0.7 on 2024-07-28 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_comments_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='time_of_listing',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
