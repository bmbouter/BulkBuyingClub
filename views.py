from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from models import OrderOpportunity, ProductForSale, Order, Purchase
from forms import PurchaseForm, PurchaseAgreementForm

@login_required
def viewOrderOpportunities(request):
    """Displays all OrderOpportunities
    
    Displays the order opportunities for the user and notifies them
    of orders they have not ordered for yet.  It passes an array of 
    2-tuples with the form (delivery_date, has_ordered_bool) to 
    OrderOpportunity.html  The variables delivery_date is a string
    and has_ordered_bool is True if the user has already ordered for
    that order.

    """
    oo = OrderOpportunity.objects.all()
    for o in oo:
        o.has_ordered_bool = _has_already_placed_order(request.user, o.pk)
    return render_to_response('OrderOpportunities.html',
                              {'oo': oo},
                              context_instance=RequestContext(request))

def _has_already_placed_order(user, order_opportunity_pk):
    """Returns True or False depending on if a user has placed their order

    This returns True if the user has an Order in for OrderOpportunity.
    False otherwise.

    Parameters:
    user -- a django user object
    order_opportunity_pk -- the primary key of the order opportunity to 
        search with

    """
    try:
        order = Order.objects.filter(order_opportunity=order_opportunity_pk).get(user=user)
        return True
    except Order.DoesNotExist:
        return False

@login_required
def viewSingleOrderOpportunity(request, pk):
    """Displays the contents of a single OrderOpportunity"""
    if request.method == "GET":
        try:
            order = Order.objects.filter(order_opportunity=pk).get(user=request.user)
            order_opportunity = OrderOpportunity.objects.get(pk=pk)
            purchases = Purchase.objects.filter(order__user=request.user).filter(order__order_opportunity=pk)
            PurchaseFormSet = formset_factory(PurchaseForm, extra=0)
            formset_initial_data = [{'qty': i.qty,
                                     'product_pk': i.pk, 
                                     'price': i.product_for_sale.price, 
                                     #'price': i.qty * i.product_for_sale.price, 
                                     'name': i.product_for_sale.name} for i in purchases]
            formset = PurchaseFormSet(initial=formset_initial_data)
            total = reduce(lambda x, y: x+y, [p.qty * p.product_for_sale.price for p in purchases], 0)
            total = total + order_opportunity.fuel_surcharge
            return render_to_response('ReadOnlyOrder.html',
                                      {'order_opportunity': order_opportunity,
                                      'formset': formset,
                                      'total': total},
                                      context_instance=RequestContext(request))
        except Order.DoesNotExist:
            order_opportunity = OrderOpportunity.objects.get(pk=pk)
            products_for_sale = ProductForSale.objects.filter(order_opportunity=pk)
            PurchaseFormSet = formset_factory(PurchaseForm, extra=0)
            formset_initial_data = [{'product_pk': i.pk, 
                                     'price': i.price, 
                                     'name': i.name} for i in products_for_sale]
            formset = PurchaseFormSet(initial=formset_initial_data)
            agreement = PurchaseAgreementForm()
            return render_to_response('PlaceOrder.html',
                                      {'order_opportunity': order_opportunity,
                                      'agreement': agreement,
                                      'formset': formset},
                                      context_instance=RequestContext(request))
    elif request.method == "POST":
        PurchaseFormSet = formset_factory(PurchaseForm)
        formset = PurchaseFormSet(request.POST)
        agreement = PurchaseAgreementForm(request.POST)
        order_opportunity = OrderOpportunity.objects.get(pk=pk)
        if formset.is_valid() and agreement.is_valid():
            order_opportunity = OrderOpportunity.objects.get(pk=pk)
            order = Order(order_opportunity=order_opportunity, user=request.user)
            order.save()
            num_purchases = 0
            for form in formset.forms:
                if int(form['qty'].data) == 0: continue
                product_for_sale = ProductForSale.objects.get(pk=form['product_pk'].data)
                purchase = Purchase(qty=form['qty'].data, 
                                    product_for_sale=product_for_sale, 
                                    order=order)
                purchase.save()
                num_purchases = num_purchases + 1
            if num_purchases == 0:
                order.delete()
        else:
            return render_to_response('PlaceOrder.html',
                                      {'order_opportunity': order_opportunity,
                                      'agreement': agreement,
                                      'formset': formset},
                                      context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('single-order-opportunity', args=[pk]))

def viewSingleOrderSummary(request, pk):
    """Displays the contents of a single OrderOpportunity"""
    order_opportunity = OrderOpportunity.objects.get(pk=pk)
    return HttpResponse('implement groups first')
