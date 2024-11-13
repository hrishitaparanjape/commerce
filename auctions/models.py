from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.name
class AuctionsListing(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    initial_bid = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return self.title

    
class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Bid by {self.user.username} of {self.amount}"

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(AuctionsListing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"
    
