from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ListingForm
from .models import User, Listing
from django.shortcuts import render, get_object_or_404


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    # Vérifie si l'user connecté a cette annonce dans sa watchlist
    on_watchlist = False
    if request.user.is_authenticated:
        on_watchlist = listing.watchers.filter(pk=request.user.pk).exists()
    
    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "on_watchlist": on_watchlist
    })
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    if request.user.is_authenticated:
        if listing.watchers.filter(pk=request.user.pk).exists():
            listing.watchers.remove(request.user)  # Retire de la watchlist
        else:
            listing.watchers.add(request.user)  # Ajoute à la watchlist
    
    return HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))


def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user 
            listing.current_price = listing.starting_bid 

            listing.save()
            return redirect("index")
        else:
            form = ListingForm()
        return render(request, "auctions/create_listing.html",{
            "form":form
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
