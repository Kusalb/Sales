# users/forms.py
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Shop, Customer, Product
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from sales.models import Employee

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'is_admin', 'is_customer', 'is_shop')


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user




class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        # fields = ('username', 'email')
        fields = ('username', 'email', 'is_admin', 'is_customer', 'is_shop')

    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"password/\">this form</a>."))

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = ('shop_name', 'contact', 'location', 'category', 'sale_per', 'branded', 'email', 'password', 'password2')



class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'address', 'email', 'gender', 'contact', 'password', 'password2')



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('image', 'product_name', 'price', 'discount', 'category')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"


