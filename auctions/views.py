from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ListingForm, BidForm
from .models import User, Listing
from django.shortcuts import render, get_object_or_404
from django.contrib import messages


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })



def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing.objects.prefetch_related('bids__user'), pk=listing_id)
    is_winner =   False
    if not listing.is_active and   request.user.is_authenticated:
        
        is_winner = listing.winner       == request.user
    #C'EST UN CODE POURL PARTIE 3, i believe in it
    if request.method == 'POST' and 'close_auction' in request.POST:
        if request.user == listing.creator:
            if listing.bids.exists():

                highest_bid = listing.bids.order_by('-amount').first()
                listing.winner = highest_bid.user
                messages.success(request, f"Auction closed! Winner : {highest_bid.user.username}")
            else:

                messages.warning(request, "No bids placed - auction  closed without winner.")
            
            listing.is_active = False
            listing.save()



            return redirect('listing_detail' , listing_id=listing.id)
        else:
            messages.error(request, "Only the creator can  close the auction.")


    

    on_watchlist = False
    if request.user.is_authenticated:
        on_watchlist = listing.watchers.filter(pk=request.user.pk).exists()

    # kod sa gen pou modifye, c'est sur je vais le faire, i'll do it
    bid_error = None
    if request.method == "POST" and "place_bid" in request.POST:
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            new_bid.listing = listing 
            new_bid.user = request.user 

            if new_bid.amount < listing.starting_bid:
                bid_error = "Bid must be at least as large as the starting price."
            elif listing.bids.exists() and new_bid.amount <= listing.bids.first().amount:
                bid_error = "Your bid must be higher the current highest bid."
            else:
                new_bid.save()
                listing.current_price = new_bid.amount 
                listing.save()
                messages.success(request, "Your bid was placed successfully")
                return redirect("listing_detail",  listing_id=listing.id)
    else:
        form = BidForm()
    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "on_watchlist": on_watchlist,
        "bid_error": bid_error,
        "form": form,
        
        'is_winner': is_winner,
    })
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    if request.user.is_authenticated:
        if listing.watchers.filter(pk=request.user.pk).exists():
            listing.watchers.remove(request.user) 
        else:
            listing.watchers.add(request.user)  
    
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


        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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
