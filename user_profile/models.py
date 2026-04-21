from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


# Create your models here.
class Profile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """

    class YearsPlaying(models.IntegerChoices):
        NEWCOMER = 1, "Less than 1 year"
        BEGINNER = 2, "1-3 years"
        INTERMEDIATE = 3, "3-5 years"
        EXPERIENCED = 4, "5-10 years"
        EXPERT = 5, "10+ years"

    class FaveSurface(models.TextChoices):
        INDOOR_HARD = "indoor_hard", "Indoor Hard"
        OUTDOOR_HARD = "outdoor_hard", "Outdoor Hard"
        CLAY = "clay", "Clay"
        GRASS = "grass", "Grass"
        CARPET = "carpet", "Carpet"

    class FaveShot(models.TextChoices):
        SERVE = "serve", "Serve"
        TOPSPIN_FOREHAND = "topspin_forehand", "Topspin Forehand"
        SLICE_FOREHAND = "slice_forehand", "Slice Forehand"
        FLAT_FOREHAND = "flat_forehand", "Flat Forehand"
        TOPSPIN_BACKHAND = "topspin_backhand", "Topspin Backhand"
        SLICE_BACKHAND = "slice_backhand", "Slice Backhand"
        FLAT_BACKHAND = "flat_backhand", "Flat Backhand"
        FOREHAND_VOLLEY = "forehand_volley", "Forehand Volley"
        BACKHAND_VOLLEY = "backhand_volley", "Backhand Volley"
        DROP_VOLLEY = "drop_volley", "Drop Volley"
        SMASH = "smash", "Smash"
        HALF_VOLLEY = "half_volley", "Half-Volley"
        LOB = "lob", "Lob"
        DROP_SHOT = "drop_shot", "Drop Shot"
        TWEENER = "tweener", "Tweener"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label="Country", null=True, blank=True)
    years_playing = models.IntegerField(choices=YearsPlaying.choices, null=True, blank=True)
    fave_surface = models.CharField(choices=FaveSurface.choices, max_length=50, null=True, blank=True)
    fave_shot = models.CharField(choices=FaveShot.choices, max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()