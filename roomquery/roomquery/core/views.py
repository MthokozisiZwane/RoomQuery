from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Property
from django.contrib.auth import login,  logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, PropertySearchForm, PropertyForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



# Create your views here.


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    return render(request, 'core/login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('property_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

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

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property_form.html'
    success_url = reverse_lazy('property_list')

    def form_valid(self, form):
        form.instance.landlord = self.request.user
        return super().form_valid(form)

class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property_form.html'
    success_url = reverse_lazy('property_list')

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.landlord

class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    template_name = 'property_confirm_delete.html'
    success_url = reverse_lazy('property_list')

    def test_func(self):
        property = self.get_object()
        return self.request.user == property.landlord