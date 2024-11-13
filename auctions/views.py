from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import AuctionsListing, Bid, Comment, User


from .models import User


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listings = AuctionsListing.objects.all()
    return render(request, "auctions/index.html", {'listings': listings})


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

@login_required
def create_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        initial_bid = request.POST.get('initial_bid')
        category = request.POST.get('category')
        image_url = request.POST.get('image_url')

        listing = AuctionsListing(
            title=title,
            description=description,
            initial_bid=initial_bid,
            category=category,
            image_url=image_url,
            user=request.user
        )
        listing.save()

    return render(request, 'auctions/create_listing.html')

@login_required
def categories(request):
    listings = AuctionsListing.objects.all()
    return render(request,'auctions/categories.html',{'listings': listings})
        
def category_listings(request):
    category_name = request.GET.get('category_name')
    filtered_listings = AuctionsListing.objects.filter(category = category_name)
    context = {
        'category_name': category_name,
        'filtered_listings': filtered_listings
    }
    return render(request, 'auctions/category_listings.html', context)

def listings_page(request):
    listing_title = request.GET.get('title')
    listings = AuctionsListing.objects.all()
    action = request.POST.get('action')
    print("Action = ", request.POST.get("action"))
    if listing_title:
        filtered_listing_by_id = listings.filter(title__iexact=listing_title)    
        if filtered_listing_by_id.exists():
            print("Listings found:", filtered_listing_by_id)
        else:
            print("No listings found with the title:", listing_title)
    else:
        filtered_listing_by_id = listings
    if request.method == 'POST':
        new_bid = request.POST.get('initial_bid') 
        comment_content = request.POST.get('comment') 
        if new_bid:
            filtered_listing_by_id.update(initial_bid=new_bid)
            bid = Bid(
                amount=new_bid,
                user=request.user,
                listing=filtered_listing_by_id.first()
            )
            print("Bid model:", bid)
            bid.save()  
        if comment_content:            
            commentobject = Comment(
                content=comment_content,
                user=request.user,
                listing=filtered_listing_by_id.first()
            )
            commentobject.save()
    if action == "delete":         
        if request.method == "POST":
            listing_id = request.POST.get("listing_id")
            listing = AuctionsListing.objects.filter(id=listing_id, user=request.user).first()
            if listing:
                listing.delete()
            listings = AuctionsListing.objects.all()
            return render(request, 'auctions/index.html', {'listings': listings})
    if action == "add_to_watch_list":
        listing_id = request.POST.get("listing_id")
        print("listing id", listing_id)
        if listing_id:
            if 'watchlist' not in request.session:
                request.session['watchlist'] = []
            if listing_id not in request.session['watchlist']:
                request.session['watchlist'].append(listing_id)
                request.session.modified = True
        filtered_listing_by_id = listings.filter(id=listing_id)    
        return render(request, 'auctions/listings_page.html', {'filtered_listing_by_id': filtered_listing_by_id, 'action_finished': 'Added to Watch List'})
    else:        
        comment_filtered = Comment.objects.filter(listing_id = filtered_listing_by_id.first().id)
        print("comment filtered=",comment_filtered)
        return render(request, 'auctions/listings_page.html', {'filtered_listing_by_id': filtered_listing_by_id, 'title': listing_title, 'comment_filtered':comment_filtered, 'listings':listings})        
    
@login_required
def watchlist_page(request):
    if request.method == "POST" and request.POST.get("action") == "remove_from_watchlist":
        listing_id = request.POST.get("listing_id")
        if listing_id and 'watchlist' in request.session:
            if listing_id in request.session['watchlist']:
                request.session['watchlist'].remove(listing_id)
                request.session.modified = True

    watchlist_ids = request.session.get('watchlist', [])
    print("Watchlist ids", watchlist_ids)
    watchlist = AuctionsListing.objects.filter(id__in=watchlist_ids)
    return render(request, 'auctions/watchlist_page.html', {'watchlist': watchlist})