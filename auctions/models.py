from django.db import models
from users.models import CustomUser
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    class Meta:
        ordering=('id',)
    def __str__(self):
        return self.name
    
class Auction(models.Model):
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE, blank=True, default=1)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='auctions',on_delete=models.CASCADE)
    thumbnail = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()

    class Meta:
        ordering=('id',)
    def __str__(self):
        return self.title
    
class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(CustomUser, related_name='bids', on_delete=models.CASCADE)

    class Meta:
        ordering=('id',)
    def __str__(self):
        return {self.bidder, self.price}
    
# Ratings
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'auction')  # un usuario solo puede puntuar una vez

    def __str__(self):
        return f"{self.user.username}, {self.auction.title} - {self.score}"
    
class Comment(models.Model):
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=1000)
    creation_date = models.DateField(auto_now_add=True)
    last_modification = models.DateField()
    auction = models.ForeignKey(Auction, related_name="auction", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return f"{self.title} - {self.user.username} - {self.auction.title}"
