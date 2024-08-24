import datetime
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Sub_Category(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Product(models.Model):
    AVAILABILITY_CHOICES = [('In stock', 'In stock'),('out of stock', 'out of stock')]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default='')
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=False, default='')
    brand = models.ForeignKey(brand, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='photos')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    date= models.DateField(auto_now_add=True)
    available = models.CharField(choices=AVAILABILITY_CHOICES,null=True,max_length=300,default='In stock')
    def __str__(self):
        return self.name


class Usercreationform(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'This email already exists'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(Usercreationform, self).__init__(*args, **kwargs)
        if 'usable_password' in self.fields:
            del self.fields['usable_password']

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(Usercreationform, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return email

class contact(models.Model):
    name = models.CharField(max_length=240)
    email = models.EmailField(max_length=240)
    subject = models.CharField(max_length=200)
    message = models.TextField()




class orders(models.Model):
    image = models.ImageField(upload_to='order/photos', default="", null=True)
    product = models.CharField(max_length=100, default='', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Quantity = models.CharField(max_length=200, default='', null=True)
    address = models.TextField(default="", null=True)
    price = models.CharField(max_length=100, default='', null=True)
    pincode = models.CharField(max_length=20, default="", null=True)
    phone = models.CharField(max_length=30, default="", null=True)
    total = models.IntegerField(default=0, null=True)
    date = models.DateField(default=datetime.date.today, null=True)

    def __str__(self):
        return self.product

