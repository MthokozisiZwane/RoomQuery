from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from . models import Property
from django.contrib.auth import login,  logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, PropertySearchForm
from django.db.models import Q

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
    context_object_name = 'properties'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        property_type = self.request.GET.get('property_type')
        min_bedrooms = self.request.GET.get('min_bedrooms')
        max_bedrooms = self.request.GET.get('max_bedrooms')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if query:
            queryset = queryset.filter(Q(address__icontains=query) | Q(description__icontains=query))
        
        if property_type and property_type != 'all':
            queryset = queryset.filter(property_type=property_type)
        
        if min_bedrooms:
            queryset = queryset.filter(bedrooms__gte=min_bedrooms)
        
        if max_bedrooms:
            queryset = queryset.filter(bedrooms__lte=max_bedrooms)
        
        if min_price:
            queryset = queryset.filter(rent_price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(rent_price__lte=max_price)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PropertySearchForm(self.request.GET)
        return context

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'core/property_detail.html'
    context_object_name = 'property'

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logged_out')
    return render(request, 'logged_out.html')
