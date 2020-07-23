from django.contrib import admin
from .models import User, AuctionListings, Bid, Comment

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class AuctionListingsAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "bid", "listing_category", "post_date")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bid", "bid_owner", "listing_target")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment", "listing_target", "comment_owner")

admin.site.register(User, UserAdmin)
admin.site.register(AuctionListings, AuctionListingsAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)