# Generated by Django 5.0.7 on 2024-09-10 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listings_comments_bids_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
