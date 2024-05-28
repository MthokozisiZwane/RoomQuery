from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Property

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    return render(request, 'core/login.html')

def register(request):
    return render(request, 'core/register.html')

class PropertyListView(ListView):
    model = Property
    template_name = 'core/property_list.html'

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'core/property_detail.html'
