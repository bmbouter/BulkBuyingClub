from django.conf.urls.defaults import *

urlpatterns = patterns('bulk_buying_club',
    url(r'^$', 'views.viewOrderOpportunities', name='order-opportunities'),
    url(r'^(?P<pk>\d+)/order/$', 'views.viewSingleOrderOpportunity', name='single-order-opportunity'),
    url(r'^(?P<pk>\d+)/summary/$', 'views.viewSingleOrderSummary', name='single-order-summary'),
)
