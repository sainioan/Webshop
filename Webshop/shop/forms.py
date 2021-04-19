from django import forms


class SearchForm(forms.Form):
    product_name = forms.CharField()
    price = forms.DecimalField()