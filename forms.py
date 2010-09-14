from django import forms

class PurchaseForm(forms.Form):
    """A PurchaseForm class for to capture multiple purchases

    This is designed to be used as a formset of purchases which
    together make up an Order, which is created at POST time

    """
    product_pk = forms.IntegerField()
    qty = forms.IntegerField(initial=0)
    price = forms.FloatField()
    name = forms.CharField()

class PurchaseAgreementForm(forms.Form):
    """This places a checkbox for the user to click"""

    agreed = forms.BooleanField(required=True)
