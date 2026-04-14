from django.db import models
from django.core.validators import MinValueValidator
from django_extensions.db.fields import AutoSlugField

# Create your models here.
DAYS_OF_WEEK_CHOICES = [
        ("monday" ,"Monday"),
        ("tuesday" ,"Tuesday"),
        ("wednesday" ,"Wednesday"),
        ("thursday" ,"Thursday"),
        ("friday" ,"Friday"),
        ("saturday" ,"Saturday"),
        ("sunday" ,"Sunday"),
    ]


class Location(models.Model):
    name = models.CharField(max_length=150)
    street_address1 = models.CharField(max_length=100)
    street_address2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    number_of_courts = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    slug = AutoSlugField(populate_from=['name'])
    
    
    def __str__(self):
        return f'{self.name}'


class Court(models.Model):
    SURFACE_CHOICES = [
        ("hard", "Hard Court"),
        ("clay", "Clay Court"),
        ("grass", "Grass Court"),
        ("carpet", "Carpet Court"),
    ]
    
    name = models.CharField(max_length=150)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="courts"
        ) 
    surface = models.CharField(max_length=50, choices=SURFACE_CHOICES, default="hard")
    outside = models.BooleanField(default=True, verbose_name="Is the court outside?")
    slug = AutoSlugField(populate_from=['name'])
    
    
    def __str__(self):
        return f'{self.name} on a {self.get_surface_display()}'


class CourtAvailability(models.Model):  
    court = models.ForeignKey(
        Court, on_delete=models.CASCADE, related_name="court_times"
        )
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK_CHOICES)
    open_time = models.TimeField(auto_now=False, auto_now_add=False)
    close_time = models.TimeField(auto_now=False, auto_now_add=False)
    
    
    def __str__(self):
        return f'{self.court.name} | {self.day} | {self.open_time} | {self.close_time}'


class Coach(models.Model):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    specialty = models.CharField(max_length=250)
    location_available = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='coaches')
    slug = AutoSlugField(populate_from=['name'])
    
    
    def __str__(self):
        return f'{self.name} ({self.nickname}) at {self.location_available.name}'


class CoachAvailability(models.Model):    
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name="coach_times")
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK_CHOICES)
    shift_start = models.TimeField(auto_now=False, auto_now_add=False)
    shift_end = models.TimeField(auto_now=False, auto_now_add=False)
    
    
    def __str__(self):
        return f'{self.coach.name} | {self.day} | {self.shift_start} | {self.shift_end}'