from django.contrib import admin
from .models import Category, Sub_Category, Product, contact,orders, brand

class ordersAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'product','Quantity')  # Fields to display in the list view



admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(contact)
admin.site.register(orders,ordersAdmin)
admin.site.register(brand)