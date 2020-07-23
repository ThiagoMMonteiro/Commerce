from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("watchlist_add/<int:al_id>/<int:user_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:al_id>/<int:user_id>", views.watchlist_remove, name="watchlist_remove"),
    path("place_bid/<int:al_id>/<int:user_id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:al_id>", views.close_auction, name="close_auction")
]
