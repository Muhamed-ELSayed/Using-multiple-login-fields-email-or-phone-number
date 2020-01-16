from django.views.generic import CreateView, FormView, TemplateView
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.validators import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


class CreateUser(CreateView):
  form_class = RegisterForm
  template_name = 'users/register.html'
  success_url = reverse_lazy('users:login')

class LoginUser(FormView):
  form_class= LoginForm
  template_name = 'users/login.html'
  success_url= reverse_lazy('users:register')

  

  

class Success_page(TemplateView):
  template_name = 'users/success_page.html'

  
