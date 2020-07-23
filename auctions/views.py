from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListings, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "auction_listings": AuctionListings.objects.filter(is_open=True)
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
                            url_listing_image=url_listing_image, listing_category=listing_category, al_owner=request.user, is_open = True)
        auction_listing.save() 
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listings.html")

def listing(request, listing_id):
    
    al = AuctionListings.objects.get(pk=listing_id)
    try:
        max_bid = al.current_bid.aggregate(Max('bid'))
        max_bid = float(max_bid["bid__max"])
        winner_bid = al.current_bid.all().get(bid=max_bid)
        winner_user = winner_bid.bid_owner
    except:
        winner_user = "al.al_owner"
    return render(request, "auctions/listing.html", {
        "al": al,
        "watchlist": al.users_whatching.all(),
        "winner_user": winner_user
    })

def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user.watchlist.all()
    })

def watchlist_add(request, al_id, user_id):
    al = AuctionListings.objects.get(pk=al_id)
    user = User.objects.get(pk=user_id)
    user.watchlist.add(al)
    return HttpResponseRedirect(reverse("listing", args=[al_id]))

def watchlist_remove(request, al_id, user_id):
    al = AuctionListings.objects.get(pk=al_id)
    user = User.objects.get(pk=user_id)
    user.watchlist.remove(al)
    return HttpResponseRedirect(reverse("listing", args=[al_id]))

def place_bid(request, al_id, user_id):
    if request.method == "POST":
        new_bid = float(request.POST["bid"])
        al = AuctionListings.objects.get(pk=al_id)
        message = None
        if new_bid < al.bid and Bid.objects.filter(listing_target=al_id).count() == 0:
            message = "The bid must be at least as large as the starting bid!"
        elif new_bid <= al.bid and Bid.objects.filter(listing_target=al_id).count() != 0:
            message = "The bid must be greater than current bid!"
        if message:
            return render(request, "auctions/error.html",{
                    "message": message,
                    "al_id": al_id
                })
        else:
            user = User.objects.get(pk=user_id)
            bid = Bid(bid=new_bid, bid_owner=user, listing_target=al)
            bid.save()

            AuctionListings.objects.filter(pk=al_id).update(bid=new_bid)

            return HttpResponseRedirect(reverse("listing", args=[al_id]))

def close_auction(request, al_id):
    al = AuctionListings.objects.get(pk=al_id)
    al.is_open = False
    al.save()

    return HttpResponseRedirect(reverse("index"))
