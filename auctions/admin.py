from django.contrib import admin
from .models import User, AuctionListings, Bid

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class AuctionListingsAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "bid", "listing_category", "post_date")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bid", "bid_owner", "listing_target")

admin.site.register(User, UserAdmin)
admin.site.register(AuctionListings, AuctionListingsAdmin)
admin.site.register(Bid, BidAdmin)