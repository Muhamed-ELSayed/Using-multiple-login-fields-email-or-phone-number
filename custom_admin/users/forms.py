from django import forms
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from .models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField

#  create Register form 
class RegisterForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('fullname', 'phone', 'email', 'password', 'password_confirm')
    widgets = {
      'fullname': forms.TextInput(attrs={'placeholder':'Enter Fullname'}),
      'phone': PhoneNumberPrefixWidget(attrs={'placeholder':'Enter Phone Number'}, initial='SA'),
      'email': forms.EmailInput(attrs={'placeholder':'Enter your Email'}),
      'password': forms.PasswordInput(attrs={'placeholder':'Enter your password'}),
      'password_confirm': forms.PasswordInput(attrs={'placeholder':'Enter your password'})
    }

  # Validation for email if exists or no
  def clean_email(self):
    data = self.cleaned_data
    email = data.get('email')

    qs = User.object.filter(email= email)
    if qs.exists():
      raise forms.ValidationError("Email is taken")
    return email

  # validation for password annd password_confirm
  def clean_password_confirm(self):
    data = self.cleaned_data
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    if password != password_confirm:
      raise forms.ValidationError("Password don't match")
    return password_confirm

  # Validation for fullname
  def clean_fullname(self, *args, **kwargs):
    data = self.cleaned_data
    fullname = data.get('fullname')

    if len(fullname) < 6:
      raise forms.ValidationError("It's very short name")
    return fullname

  #  Validation for phone number
  def clean_phone(self, *args, **kwargs):
    data = self.cleaned_data
    phone = data.get('phone')
    qs = User.object.filter(phone=phone)
    if qs.exists():
      raise forms.ValidationError('Phone is taken')
    return phone

  def save(self, commit=True):
    user = super(RegisterForm, self).save(commit=False)
    user.set_password(self.cleaned_data.get('password'))
    if commit:
      user.save()
    return user


# Create form for login with email or phone number
class LoginForm(forms.Form):
  phone_email= forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Enter your Email or Phone'}))

  password = forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))

  class Meta:
    fields = '__all__'


  def clean(self, *args, **kwargs):
    data = self.cleaned_data
    phone_email = data.get('phone_email')
    password = data.get('password')
    user = authenticate(email_or_phone=phone_email, password=password)

    if not user:
      raise forms.ValidationError('Sorry, that login was invalid. Please try again.')
    else:
      return data
  
  def login(self, request):
    request =self.request
    data = self.cleaned_data
    phone_email = data.get('phone_email')
    password = data.get('password')
    user = authenticate(request, username= phone_email, password=password)
    return user


  