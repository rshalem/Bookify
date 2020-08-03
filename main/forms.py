"""
clean () is a classwide function, whereas clean <fieldname> is invoked when is_valid is called
& returns a value,
clean() is called after all other validators option & methods
because what if a clean<fieldname> methods raise Validation Error & doesnt return any value
& that value is not stored in cleaned_data dict. Hence inside clean() we use get('fieldname', '') this empty is for
safer side
"""

from django import forms
from django_countries.widgets import CountrySelectWidget
from django.forms import ModelForm, TextInput, EmailInput

from .models import Address


class AddressForm(ModelForm):

    # providing extra fields that will be required in the model form
    # eg: house_colour = models.CharField(max_length = 10)
    class Meta:
        model = Address
        exclude = ['shipping_user']

        widgets = {
            'shipping_first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'shipping_last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter second name'}),
            'shipping_user_email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter valid email'}),
            'shipping_address_one': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}),
            'shipping_address_two': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}),
            'shipping_city': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'phone_number': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter registered number'}),
            'shipping_house_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'House no.'}),
            'shipping_country': CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Select country'}),
            'shipping_state': TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'shipping_zip': TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
        }

    def clean_shipping_user_email(self):
        # get the field value from cleaned_data dict, self is the form instance
        value = self.cleaned_data['shipping_user_email']
        # checking if value ends with @gmail.com
        if not value.endswith('@gmail.com'):
            raise forms.ValidationError('Please use valid gmail account')

        # always return the value
        return value

    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        if not value.isdigit():
            # this error key is added to the error dict
            raise forms.ValidationError('Please enter a valid phone number')

        return value

    def clean(self):
        # Call clean() to explicitly call the base form class ie ModelForm
        # since its a class wide method, overriding is done
        super(AddressForm, self).clean()
        first_name = self.cleaned_data.get('shipping_first_name', '')
        last_name = self.cleaned_data.get('shipping_last_name', '')
        address_one = self.cleaned_data.get('shipping_address_one', '')
        address_two = self.cleaned_data.get('shipping_address_two', '')

        if first_name == last_name:
            raise forms.ValidationError("First name & last name fields can't be same")

        elif address_one == address_two:

            message = "Address 1 & 2 can't be same"
            self.add_error('shipping_address_two', message)
            # or
            # self.add_error('shipping_first_name', forms.ValidationError(message))

# class PaymentForm(ModelForm):
#     class Meta:
#         model = Payment
#         fields = '__all__'