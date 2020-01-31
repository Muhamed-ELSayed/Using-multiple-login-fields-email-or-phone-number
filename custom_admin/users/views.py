from django.views.generic import CreateView, FormView, TemplateView
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


class WelcomePage(TemplateView):
  template_name = 'welcome_page.html'



class AjaxableResponseMixinRegister:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        error = form.errors.as_json()
        if self.request.is_ajax():
            return HttpResponse(error, status=400, content_type='application/json')
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            form.save()
            data={'user':True}
            return JsonResponse(data)
        else:
            return response

class AjaxableResponseMixinLogin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        error = form.errors.as_json()
        if self.request.is_ajax():
            return HttpResponse(error, status=400, content_type='application/json')
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            form.login()
            data={'user':True}
            return JsonResponse(data)
        else:
            return response

class CreateUser(AjaxableResponseMixinRegister, FormView):
  form_class = RegisterForm
  template_name = 'users/register.html'
  success_url = reverse_lazy('users:login')

  def get(self, request,*args, **kwargs):
    data= dict()
    context = {'form':self.form_class}
    data['html_form'] = render_to_string(self.template_name, context=context, request=request)
    return JsonResponse(data)

class LoginUser(AjaxableResponseMixinLogin, FormView):
  form_class= LoginForm
  template_name = 'users/login.html'
  success_url= reverse_lazy('users:register')

  def get(self, request, *args, **kwargs):
    data = dict()
    context = {'form':self.form_class}
    data['html_form'] = render_to_string(self.template_name, context=context, request=request)
    return JsonResponse(data)


