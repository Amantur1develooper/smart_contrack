from django.db import models
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
import uuid
import hashlib


class UserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, phone,password=None):
        user = self.model(
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            phone = phone,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email,firstname,lastname,phone,password=None):
        user = self.create_user(
            email=email,
            password=password,
            firstname = firstname,
            lastname = lastname,
            phone = phone,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    # id = models.CharField(max_length=200, default=uuid.uuid4,unique=True,primary_key=True)
    email = models.EmailField(null=False, max_length=100,unique=True)
    idpassword = models.CharField(max_length=22,blank=True, null=True, verbose_name='id password')
    image = models.ImageField(verbose_name='изображение', upload_to='user_images/', blank=True, null=True)
    firstname = models.CharField(null=False, max_length=100)
    lastname = models.CharField(null=False, max_length=100)
    phone = models.IntegerField(null=False,unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname','lastname','phone']

    objects = UserManager()

    def __str__(self):
        return self.email + ", " + self.firstname
    
    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    
from django.db import models

class Contract(models.Model):
    index = models.IntegerField(null=True, blank=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bought_contracts')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sold_contracts')
    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_terms = models.TextField()
    delivery_terms = models.TextField()
    warranty = models.TextField()
    dispute_resolution = models.TextField()
    podpis1 = models.FileField(upload_to='podpisi1')
    podpis2 = models.FileField(upload_to='podpisi2')
    timestamp = models.DateTimeField(auto_now_add=True,null=True, blank=True, verbose_name='создания блока')
    previous_hash = models.CharField(max_length=64,null=True, blank=True)
    hash = models.CharField(max_length=64, blank=True,null=True)
    
    def save(self, *args, **kwargs):
        self.hash = self.compute_hash()
        super(Contract, self).save(*args, **kwargs)
        
    def __str__(self):
        return "контракт{}".format(self.index)
    def compute_hash(self):
        block_string = "{}{}{}{}{}{}{}{}{}{}{}{}".format(self.index,self.buyer,self.seller,self.item,self.price,self.payment_terms,
                    self.delivery_terms,self.warranty,self.dispute_resolution,self.podpis1,self.podpis2,self.timestamp, self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()
        
    

class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Delivery(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=255)
    delivery_date = models.DateTimeField()
