from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Property, Booking
from django.contrib.auth import login,  logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, PropertySearchForm, PropertyForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserUpdateForm, BookingForm
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
    properties = Property.objects.all()
    return render(request, 'core/index.html', {'properties': properties})

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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
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
    

# Adding views for booking

@login_required
def book_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tenant = request.user
            booking.property = property
            booking.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'core/book_property.html', {'form': form, 'property': property})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(tenant=request.user)
    return render(request, 'core/booking_list.html', {'bookings': bookings})

# Booking views

@login_required
@user_passes_test(lambda u: u.user_type == 'landlord')
def landlord_bookings(request):
    properties = Property.objects.filter(landlord=request.user)
    bookings = Booking.objects.filter(property__in=properties)
    return render(request, 'core/landlord_bookings.html', {'bookings': bookings})

@login_required
@user_passes_test(lambda u: u.user_type == 'landlord')
def respond_booking(request, booking_id, response):
    booking = get_object_or_404(Booking, id=booking_id, property__landlord=request.user)
    if response == 'accept':
        booking.landlord_response = 'accepted'
        booking.status = 'confirmed'
    elif response == 'reject':
        booking.landlord_response = 'rejected'
        booking.status = 'cancelled'
    booking.save()
    return redirect('landlord_bookings')

class TenantBookingsView(ListView):
    model = Booking
    template_name = 'core/tenant_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(tenant=self.request.user).order_by('booking_date')