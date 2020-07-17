from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
        listing_title = models.CharField(max_length=64)
        listing_description = models.CharField(max_length=256)
        bid = models.FloatField()
        url_listing_image = models.CharField(blank = True, max_length=512)
        listing_category = models.CharField(blank = True, max_length=64)
        post_date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='post date')

        def __str__(self):
            return f"{self.listing_title}: {self.listing_description} Starting Bid: {self.bid} Category: {self.listing_category}"