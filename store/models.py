from django.db import models
from djongo import models as mongo


# Create your models here.
class CarCategory(models.Model):
    _id = mongo.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    _id = mongo.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = mongo.EmbeddedField(model_container=CarCategory)
    images = models.JSONField()

    def __str__(self):
        return self.name 
    
  
class Client(models.Model):
    _id = mongo.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    identification = models.CharField(max_length=100)
    type = models.CharField(max_length=100,default='Client')
    
    def __str__(self):
        return self.name + ' ' + self.lastName


class ShoppingCar(models.Model):
    _id = mongo.ObjectIdField(primary_key=True)
    ip = models.GenericIPAddressField()
    client = mongo.ArrayField(model_container=Client, null=True)
    products = models.JSONField()


class OrderDetails(models.Model):
    _id = mongo.ObjectIdField(primary_key=True)
    quantity = models.IntegerField()
    product =  mongo.ArrayField(model_container = Car)

   

class Order(models.Model):
    _id = mongo.ObjectIdField(primary_key=True)
    fecha = models.DateField()
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    detalle = mongo.EmbeddedField(model_container=OrderDetails)
    objects = mongo.DjongoManager()


class PromoCode(models.Model):
    _id = mongo.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()    
    def __str__(self):
        return self.name 