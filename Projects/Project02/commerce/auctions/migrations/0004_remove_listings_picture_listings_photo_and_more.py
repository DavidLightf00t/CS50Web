# Generated by Django 5.0.6 on 2024-07-17 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listings_category_listings_starting_bid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='picture',
        ),
        migrations.AddField(
            model_name='listings',
            name='photo',
            field=models.URLField(default='https://t4.ftcdn.net/jpg/04/70/29/97/360_F_470299797_UD0eoVMMSUbHCcNJCdv2t8B2g1GVqYgs.jpg'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='description',
            field=models.TextField(),
        ),
    ]
