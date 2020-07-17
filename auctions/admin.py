from django.contrib import admin
from .models import User, AuctionListings

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class AuctionListingsAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "bid", "listing_category", "post_date")

admin.site.register(User, UserAdmin)
admin.site.register(AuctionListings, AuctionListingsAdmin)