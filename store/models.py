from django.conf import settings
from django.db import models
from django.urls import reverse



class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

class PallyManager(models.Manager):
    def get_queryset(self):
        return super(PallyManager, self).get_queryset().filter(is_active=True)


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
    title = models.CharField(max_length=255)


class Price(models.Model):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE, related_name='related_quantity')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.price} per {self.unit.title}'

    class Meta:
        pass

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator', null=True, blank=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255)
    price = models.OneToOneField(Price, on_delete=models.CASCADE, related_name='related_product')
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title

class Pally(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pally_creator')
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    price_per_slot = models.DecimalField(max_digits=5,decimal_places=2)
    max_num_slot = models.IntegerField()
    slug = models.SlugField(max_length=255)
    discount = models.DecimalField(max_digits=5,decimal_places=2)
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    pallies = PallyManager()

    def get_absolute_url(self):
        return reverse('store:pally_detail', args=[self.slug])