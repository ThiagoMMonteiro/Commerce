# Generated by Django 3.0.8 on 2020-07-22 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionlistings_al_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='is_open',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]