# Generated by Django 5.0.7 on 2024-08-19 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_watchlist_id_alter_listings_listing_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='id',
        ),
        migrations.AlterField(
            model_name='listings',
            name='listing_id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
