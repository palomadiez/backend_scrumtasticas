from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from auctions.models import Auction  

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('user', 'auction')  # un usuario solo puede puntuar una vez

    def __str__(self):
        return f"{self.user.username} → {self.auction.title}: {self.score}"
