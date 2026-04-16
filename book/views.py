from django.shortcuts import render
from .models import Location

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
    return "x"