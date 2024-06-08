from django.db import models

# Create your models here.
class Num(models.Model):
    val=models.IntegerField(unique=True)
    

