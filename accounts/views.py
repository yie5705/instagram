from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Create your views here.
class UserCreateView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'accounts/register_done.html'
