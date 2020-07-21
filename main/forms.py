"""
clean () is a classwide function, whereas clean <fieldname> is invoked when is_valid is called
& returns a value,
clean() is called after all other validators option & methods
because what if a clean<fieldname> methods raise Validation Error & doesnt return any value
& that value is not stored in cleaned_data dict. Hence inside clean we use get('fieldname', '') this empty is for
safer side
"""


from django import forms
from django.forms import ModelForm

from .models import Address

class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['shipping_user']
        # widgets = {
        #     'shipping_first_name':
        # }

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
        # Call clean() to explicitly call the base form class
        # since its a class wide method, overriding is done
        super(AddressForm, self).clean()
        first_name = self.cleaned_data.get('shipping_first_name', '')
        last_name = self.cleaned_data.get('shipping_last_name', '')
        if first_name == last_name:
            raise forms.ValidationError("First name & last name fields can't be same")
            # or
            # message = "First name & last name fields can't be same"
            # self.add_error('shipping_first_name', message)
            # or
            # self.add_error('shipping_first_name', forms.ValidationError(message))