from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_image_file_extension
from .managers import CustomUserManager
from django.utils import timezone
import random 

import random 


class User(AbstractUser):
    username = None
    email= models.EmailField(("email address"), unique=True)
    newsletter= models.BooleanField(default=True, help_text="Do you want to receive the newsletter?")
    ws_channel_name= models.CharField(max_length=300, blank=True, null=True)
    last_online= models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def clean(self):
        super().clean()
        self.email = self.email.lower()

    def save(self, *args, **kwargs):
        is_created = self._state.adding
        self.clean()  # Ensure the email is normalized
        
        super().save(*args, **kwargs)

        if is_created:
            Profile.objects.create(user=self)

    def __str__(self):
        return self.email


def generate_referral_code():
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    avatar= models.ImageField(
        upload_to="avatars/",
        default="default.jpeg",
        null=True,
        blank=True,
        validators=[validate_image_file_extension],
    )
    phone_number= models.CharField(max_length=15, blank=True, null=True, unique=True)

    referral_code= models.CharField(max_length=6, unique=True, default=generate_referral_code, blank=True)
    total_referrals= models.IntegerField(default=0)


    def create_random(self):
        return "".join([str(random.randint(0, 9)) for _ in range(6)])

    def save(self, *args, **kwargs):
        if not self.referral_code:
            referal_codee = self.create_random()
            # print('ur reff is ',referal_codee)
            if Profile.objects.filter(referral_code=referal_codee).exists():
                while Profile.objects.filter(referral_code=referal_codee).exists():
                    referal_codee = self.create_random()
                    # print("new ref code",referal_codee)
                    self.referral_code = referal_codee
            self.referral_code = referal_codee
        super().save(*args, **kwargs)
    

    def __str__(self):
        return str(self.user)
