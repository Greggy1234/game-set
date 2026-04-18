from django.shortcuts import render, get_object_or_404
from .models import Location, Coach, Court
from collections import defaultdict
from datetime import datetime, timedelta, date

# Create your views here.
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def book_overview(request):
    locations = Location.objects.all()
    
    context = {
        "locations": locations,
    }
    
    return render(request, "book/book-overview.html", context)


def court_book(request, slug):
    court = get_object_or_404(Court, slug=slug)
    
    times = {}
    opening_times = {}
    slot_time = 60
    final_slots = {}
    
    for ca in court.court_times.all():
        times[ca.day] = ca
    
    for day in days:
        if day in times:
            ca = times[day]                
            opening_times[day] = f'{ca.open_time.strftime("%I%p")} - {ca.close_time.strftime("%I%p")}'
            current_time = datetime.combine(date.today(),ca.open_time)
            end_time = datetime.combine(date.today(),ca.close_time)
            slots = []
            while current_time < end_time:
                slots.append(current_time.strftime("%H:%M"))
                current_time += timedelta(minutes = slot_time)
            final_slots[day] = slots
    
    context = {
        "court": court,
        "final_slots": final_slots,
    }
    
    return render(request, "book/book-court.html", context)


def coach_overview(request):
    coaches = Coach.objects.all()
    
    context = {
        "coaches": coaches,
    }
    
    return render(request, "book/coaches.html", context)