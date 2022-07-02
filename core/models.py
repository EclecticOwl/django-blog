from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



THEME_CHOICES = [
    ('dm', 'main'),
    ('lm', 'light')
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    theme = models.CharField(choices=THEME_CHOICES, max_length=100, default='main')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username


# The following is for signals to connect the user model and the profile model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
        )

@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    if created == False:
        instance.user.first_name = instance.first_name
        instance.user.last_name = instance.last_name
        instance.user.email = instance.email
        instance.user.save()
        




