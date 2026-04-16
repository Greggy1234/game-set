from django.shortcuts import render
from .models import Location, Coach

# Create your views here.
def book_overview(request):
    locations = Location.objects.all()
    
    context = {
        "locations": locations,
    }
    
    return render(request, "book/book-overview.html", context)


def court_detail(request, pk):
    return "X"


def coach_overview(request):
    coaches = Coach.objects.all()
    
    context = {
        "coaches": coaches,
    }
    
    return render(request, "book/coaches.html", context)