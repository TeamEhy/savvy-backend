from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30)
    cover_img = models.ForeignKey('Image', on_delete=models.PROTECT, related_name='cover_img_item')
    date_added = models.DateField(auto_now_add=True)
    currency = models.CharField(max_length=3)
    # seller = models.ForeignKey('Seller', on_delete=models.PROTECT)

# class ItemCategory(models.Model):
#     item = models.ForeignKey('Item', on_delete=models.PROTECT)
#     category = models.ForeignKey('Category', on_delete=models.PROTECT)

class ItemImage(models.Model):
    item = models.ForeignKey('Item', on_delete=models.PROTECT)
    img = models.ForeignKey('Image', on_delete=models.PROTECT)

class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ForeignKey('Image', on_delete=models.PROTECT)
    rank = models.CharField(max_length=30)
    accepted_payment = models.CharField(max_length=30)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.ForeignKey('Item', on_delete=models.PROTECT, related_name='item_cart')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp_added = models.CharField(max_length=30)
    currency = models.CharField(max_length=3)

class Image(models.Model):
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return '%s %s' % (str(self.pk), str(self.file))

class Category(models.Model):
    name = models.CharField(max_length=255)
    img = models.ForeignKey('Image', on_delete=models.PROTECT)

class Transaction(models.Model):
    timestamp = models.CharField(max_length=30)
    item = models.ForeignKey('Item', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    quantity = models.IntegerField()
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    type_payment = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
