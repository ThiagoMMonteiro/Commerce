from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListings


def index(request):
    return render(request, "auctions/index.html", {
        "auction_listings": AuctionListings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        listing_title = request.POST["listing_title"].capitalize()
        listing_description = request.POST["listing_description"]
        starting_bid = float(request.POST["starting_bid"])
        url_listing_image = request.POST["url_listing_image"]
        listing_category = request.POST["listing_category"]

        auction_listing = AuctionListings(listing_title=listing_title, listing_description=listing_description, bid=starting_bid, 
                            url_listing_image=url_listing_image, listing_category=listing_category)
        auction_listing.save() 
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listings.html")

def listing(request, listing_id):
    al = AuctionListings.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "al": al
    })

def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user.watchlist.all()
    })