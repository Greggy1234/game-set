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
    location = court.location
    coaches = location.coaches.all()
    coach_1 = coaches[0]
    coach_2 = coaches[1]
    
    times = {}
    coach_1_times = defaultdict(list)
    coach_2_times = defaultdict(list)
    final_slots = {}
    coach_1_slots = {}
    coach_2_slots = {}
    
    for ca in court.court_times.all():
        times[ca.day] = ca
    
    for ca in coach_1.coach_times.all():
            coach_1_times[ca.day].append(ca)
    
    for ca in coach_2.coach_times.all():
            coach_2_times[ca.day].append(ca)
    
    for day in days:
        if day in times:
            ca = times[day]
            current_time = datetime.combine(date.today(),ca.open_time)
            end_time = datetime.combine(date.today(),ca.close_time)
            slots = []
            while current_time < end_time:
                slots.append(current_time.strftime("%H:%M"))
                current_time += timedelta(minutes = 60)
            final_slots[day] = slots
        if day in coach_1_times:
            ca_1_slots = []
            for ca in coach_1_times[day]:
                current_time = datetime.combine(date.today(),ca.shift_start)
                end_time = datetime.combine(date.today(),ca.shift_end)
                while current_time < end_time:
                    ca_1_slots.append(current_time.strftime("%H:%M"))
                    current_time += timedelta(minutes = 60)
            coach_1_slots[day] = ca_1_slots
        if day in coach_2_times:
            ca_2_slots = []
            for ca in coach_2_times[day]:
                current_time = datetime.combine(date.today(),ca.shift_start)
                end_time = datetime.combine(date.today(),ca.shift_end)
                while current_time < end_time:
                    ca_2_slots.append(current_time.strftime("%H:%M"))
                    current_time += timedelta(minutes = 60)
            coach_2_slots[day] = ca_1_slots
    
    context = {
        "court": court,
        "final_slots": final_slots,        
        "coach_1": coach_1,
        "coach_2": coach_2,
        "coach_1_slots": coach_1_slots,
        "coach_2_slots": coach_2_slots,
    }
    
    return render(request, "book/book-court.html", context)


def coach_overview(request):
    coaches = Coach.objects.all()
    
    context = {
        "coaches": coaches,
    }
    
    return render(request, "book/coaches.html", context)