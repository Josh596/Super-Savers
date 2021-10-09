from django.contrib import admin
from .models import Category, Pally, Price, Product, Unit

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'price',
                    'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    readonly_fields = ('id',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Pally)
class PallyAdmin(admin.ModelAdmin):
    list_display = ['author', 'slug', 'price_per_slot',
                    'max_num_slot', 'created_on']
    list_filter = ['is_active']
    list_editable = ['price_per_slot']
    prepopulated_fields = {'slug': ('author','expiry_date')}

admin.site.register(Unit)
admin.site.register(Price)
