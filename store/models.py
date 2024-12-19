from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name
    
    def get_current_cart_total_items(self):
        order, created = Order.objects.get_or_create(customer=self, complete=False)
        return order.order_total_items()
        

class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    
    def __str__(self):
        return self.name

    def getImage(self):
        try:
            url = self.image.url
        except (FileNotFoundError, ValueError):
            url = settings.STATIC_URL + 'images/placeholder.png'
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=False, blank=False)
    
    def __str__(self):
        return str(self.id)

    def order_total_price(self):
        items = self.orderitem_set.all()
        total_value = 0
        for i in items:
            total_value += i.total_price()
        return total_value
    
    def order_total_items(self):
        items = self.orderitem_set.all()
        return sum(i.quantity for i in items)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
