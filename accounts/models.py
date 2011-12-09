from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    motto = models.CharField(max_length=333, blank=True)
    zeologin = models.CharField(max_length=128, blank=True)
    zeopass = models.CharField(max_length=128, blank=True)
    withings_oauth_token = models.CharField(max_length=255, blank=True)
    withings_oauth_verifier = models.CharField(max_length=255, blank=True)
    withings_user_id = models.IntegerField()



User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile