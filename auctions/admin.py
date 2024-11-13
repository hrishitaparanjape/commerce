from django.contrib import admin
from .models import AuctionsListing, Bid, Comment, User

admin.site.register(AuctionsListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User)

# Register your models here.
