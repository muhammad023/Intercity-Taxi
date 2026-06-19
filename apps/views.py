from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, FormView, DetailView, DeleteView


# Create your views here.

class RegisterView(TemplateView):
    template_name = 'register.html'

