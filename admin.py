from django.contrib import admin
from bulk_buying_club.models import ProductForSale, OrderOpportunity, Purchase, Order

#class ProductAdmin(admin.ModelAdmin):
#    list_display = ('name', 'default_price')

class ProductForSaleAdmin(admin.TabularInline):
    model = ProductForSale
    extra = 0

class OrderOpportunityAdmin(admin.ModelAdmin):
    inlines = (ProductForSaleAdmin,)

#class PurchaseAdmin(admin.TabularInline):
#    model = Purchase
#    extra = 0 

#class OrderAdmin(admin.ModelAdmin):
#    inlines = (ProductOrderAdmin,)

#admin.site.register(Product, ProductAdmin)
admin.site.register(OrderOpportunity, OrderOpportunityAdmin)
admin.site.register(Purchase)
#admin.site.register(ProductOrder)
admin.site.register(Order)
