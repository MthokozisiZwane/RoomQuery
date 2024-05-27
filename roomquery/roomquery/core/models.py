from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type="tenant"):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=email, user_type=user_type)
        user.set_pasword(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password, user_type="admin")
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=[("tenant", "Tenant"),("landlord", "Landlord")])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None)
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff


# The property model

class Property(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.address} - {self.property_type}"

    