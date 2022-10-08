from django.db import models

# Create your models here.
class atten(models.Model):
    id=models.IntegerField(primary_key=True)
    day=models.CharField(max_length=20)
    mudeem=models.IntegerField()
    mudeem_hour=models.IntegerField()

    najim=models.IntegerField()
    najim_hour=models.IntegerField()

    nijam=models.IntegerField()
    nijam_hour=models.IntegerField()

class work(models.Model):
    number=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    quantity=models.IntegerField()
    price=models.IntegerField()
