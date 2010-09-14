from django.db import models
from django.contrib.auth.models import User

price_max_digits = 5 # This value includes the two decimal digits

#class Product(models.Model):
#    """Stores possible products for sale during an OrderOpportunity
#
#    Fields:
#    name -- the name of the Product
#    default_price -- the default price the product has when added to an
#        OrderOpportunity
#
#    """
#    name = models.CharField(max_length=128, unique=True)
#    default_price = models.DecimalField(max_digits=price_max_digits,
#                                            decimal_places=2)
#
#    def __unicode__(self):
#        return self.name

class ProductForSale(models.Model):
    """A product being offered for a given OrderOpporunity

    Attributes:
    name -- the name of the ProductForSale
    order_opportunity -- the OrderOpportunity this ProductForSale is for
    price -- the actual price of product for this objects OrderOpportunity

    """
    name = models.CharField(max_length=128, unique=True)
    order_opportunity = models.ForeignKey('OrderOpportunity')
    price = models.DecimalField(max_digits=price_max_digits, decimal_places=2)

    def __unicode__(self):
        return '$%s %s' % (self.price, self.name)

    class Meta:
        verbose_name_plural = "Products for Sale"

class OrderOpportunity(models.Model):
    """Stores an bulk buying ordering opportunity

    OrderingOpportunities are represent an opportunity for customers to
    place a bulk-buying purchase order.  Orders may be place for a given
    OrderOpportunity until midnight on the night of the close_date.
    An OrderOpportunity will be delivered on delivery_date.

    """
    close_date = models.DateField()
    delivery_date = models.DateField()
    fuel_surcharge = models.DecimalField(max_digits=price_max_digits,
                                             decimal_places=2)
    #orders = models.ForeignKey('Order', blank=True, null=True)

    def __unicode__(self):
        return 'Order Delivery on %s' % self.delivery_date

    class Meta:
        verbose_name_plural = "Order Opportunities"

class Order(models.Model):
    """A User's collection of Purchases for an OrderOpportunity"""

    order_opportunity = models.ForeignKey('OrderOpportunity')
    user = models.ForeignKey(User) 

    def __unicode__(self):
        return '%s order for delivery on %s' % (self.user.username, self.order_opportunity.delivery_date)
    
class Purchase(models.Model):
    """Records a customer purchasing a quantity of a ProductForSale"""
    qty = models.IntegerField()
    product_for_sale = models.ForeignKey('ProductForSale')
    order = models.ForeignKey('Order')
