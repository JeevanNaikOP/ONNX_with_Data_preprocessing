from django.db import models

# Create your models here.
class scoringDataBase(models.Model):
    Id = models.AutoField(primary_key=True)
    Amount = models.CharField(max_length=100)
    Card = models.CharField(max_length=100)
    Errors = models.CharField(max_length=100)
    Merchant_city = models.CharField(max_length=100)
    Merchant_name = models.CharField(max_length=100)
    Merchant_state = models.CharField(max_length=100)
    Use_chip = models.CharField(max_length=100)
    User = models.CharField(max_length=100)
    Zip = models.CharField(max_length=100)
    IsFraud = models.CharField(max_length=100)
