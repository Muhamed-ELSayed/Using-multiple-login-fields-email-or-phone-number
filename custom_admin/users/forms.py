from django import forms
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from .models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Row, Column, Submit, Layout

# Create Register Form
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
  
  # custom shape via crispy form
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    for f in self.fields:
      field = self.fields.get(f)
      field.label = False
    
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Row(
          Column('fullname', css_class='input-field col12 custom-input'),
          Column('phone', css_class='input-field col12 custom-phone custom-input'),
          Column('email', css_class='input-field col12 custom-input'),
          Column('password', css_class='input-field col12 custom-input'),
          Column('password_confirm', css_class='input-field col12 custom-input'),
        ),
        

      Submit('submit', 'Register', css_class='btn')
    )
   


  # Validation for email if exists or no
  def clean_email(self):
    data = self.cleaned_data
    email = data.get('email')

    qs = User.objects.filter(email= email)
    if qs.exists():
      raise forms.ValidationError("Email is taken")
    return email

  # validation for password and password_confirm
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

  #  Validation for phone number if phone number is exists or no
  def clean_phone(self, *args, **kwargs):
    data = self.cleaned_data
    phone = data.get('phone')
    qs = User.objects.filter(phone=phone)
    if qs.exists():
      raise forms.ValidationError('Phone is taken')
    return phone


  # after validation save user in db
  def save(self, commit=True):
    user = super(RegisterForm, self).save(commit=False)
    user.set_password(self.cleaned_data.get('password'))
    if commit:
      user.save()
    return user


# Create form for login with email or phone number
class LoginForm(forms.Form):
  class Meta:
    model = User
    fields = ('email', 'password')

  phone_email= forms.CharField(max_length=255, label='Phone/Email',widget=forms.TextInput(attrs={'placeholder':'Enter your Email or Phone'}))

  password = forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    for f in self.fields:
      field = self.fields.get(f)
      field.label = False

    
    self.helper = FormHelper()
    self.helper.layout= Layout(
      Div(
        Row(
        Column('phone_email', css_class='input-field col12 custom-input'),
        css_class = 'row'
        ),

        Row(
          Column('password', css_class='input-field col12 custom-input'),
          css_class='row'
        ),
      ),

      Submit('submit', 'Sign in')
      
    )



  def clean(self, *args, **kwargs):
    data = self.cleaned_data
    phone_email = data.get('phone_email')
    password = data.get('password')
    user = authenticate(email_or_phone=phone_email, password=password)

    if not user:
      qs = User.objects.filter(email = phone_email)
      qp = User.objects.filter(phone = phone_email)
      if not qp.exists() and not qs.exists():
        raise forms.ValidationError('Email or Phone number not found.')
      else:
        raise forms.ValidationError('Sorry, password is wrong.')
    else:
      return data
  
  def login(self):
    data = self.cleaned_data
    phone_email = data.get('phone_email')
    password = data.get('password')
    user = authenticate(email_or_phone=phone_email, password=password)
    return user
