from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from . models import Property
from django.contrib.auth import login
from .forms import CustomUserCreationForm

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

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a desired page after sign-up
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})