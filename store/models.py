from random import randint
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify 
from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver
from account.models import UserBase
from vendor.models import Vendor



class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

class PallyManager(models.Manager):
    def get_queryset(self):
        return super(PallyManager, self).get_queryset().filter(available_slots__gt = 0, expiry_date__lt = timezone.now() )


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class Unit(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f'{self.title}'


class Price(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='related_quantity')
    quantity = models.DecimalField(max_digits=7, decimal_places=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.price} per {self.quantity} {self.unit.title}(s)'

    class Meta:
        pass

class Product(models.Model):
    categories = models.ManyToManyField(Category, related_name='%(app_label)s_%(class)s_related', blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=50, null=True, blank=True)
    price = models.OneToOneField(Price, on_delete=models.CASCADE, related_name='related_product')
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Product Discount in %', default=0)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    products = ProductManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if Product.objects.filter(title=self.title).exists():
            extra = str(randint(1, 10000))
            self.slug = slugify(self.title) + "-" + extra
        else:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def get_discount_price(self):
        price = self.price.price
        discount = 100 - self.discount
        discount_price = float(discount)/100 * float(price)

        return discount_price

    def __str__(self):
        return self.title

class Pally(models.Model):
    author = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='pally_creator', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_per_slot = models.OneToOneField(Price, on_delete=models.CASCADE, related_name='related_pally')
    max_num_slot = models.IntegerField()
    available_slots = models.IntegerField()
    members = models.ManyToManyField(UserBase)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    discount = models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    pallies = PallyManager()
    objects = models.Manager()


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.title)
        if not self.available_slots:
            self.available_slots = self.max_num_slot
        super(Pally, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:pally_detail', args=[self.id,self.slug])

    def get_empty_slot(self):
        return self.available_slots

    def get_filled_slots(self):
        return self.max_num_slot - self.available_slots

    def __str__(self) -> str:
        return f'{self.product.title} - {self.max_num_slot}'


