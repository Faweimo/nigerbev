from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# from voucher.views import acknowlege


# user Manager 
class UserManager(BaseUserManager):
    def create_user(self, username, user_type,email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            user_type=user_type
            
            # full_name = full_nam/,
            
        )
        user.set_password(password)
        # user.user_type = 4
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, user_type,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            user_type = user_type
            
        )
        user.user_type =1
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        
        user.save(using=self._db)
        return user

# Custom User 
class User(AbstractBaseUser):
    username            = models.CharField(max_length=50, unique=True,blank=True,null=True)
    # full_name          = models.CharField(max_length=50)
    email               = models.EmailField(max_length=100, unique=True,blank=True,null=True)
    is_staff            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=False)
    is_superuser       = models.BooleanField(default=False)
    user_type_choices   = ((1,'is_centraladmin'),
                            (2,'is_acknowleger'),
                            (3,'is_manager'),
                            (4,'is_client')                         
                            
                            )
    user_type           = models.IntegerField(choices = user_type_choices,blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','user_type']

    objects = UserManager()

#custom user review name
    # def full_name(self):
    #     return f'{self.full_name}'

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, add_label):
        return True


""" CLIENT """
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    full_name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.user.email)

    class Meta:        
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'     
