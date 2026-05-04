from django.shortcuts import get_object_or_404
from datetime import datetime
from book.models import Court, Coach


def booking_items(request):
    booking_items = []
    total_booking_amount = 0
    number_of_bookings = 0
    bookings = request.session.get('bookings', {})
    
    for court_id, dates in bookings.items():
        court = get_object_or_404(Court, id=court_id)
        for date, times in dates.items():
            booking_date = date
            date_as_date = datetime.strptime(booking_date, "%Y-%m-%d")
            date_human_readable = date_as_date.strftime("%A, %B %#d, %Y")
            for time, info in times.items():
                booking_time = time
                coach_id = info["coach"]
                booking_cost = int(info["cost"])
                total_booking_amount += int(info["cost"])
                booking_coach = None
                if coach_id and coach_id != "None":
                    booking_coach = get_object_or_404(Coach, id=coach_id)
                number_of_bookings += 1
                booking_items.append({
                    "booking_court": court,
                    "booking_date": booking_date,
                    "booking_time": booking_time,
                    "booking_coach": booking_coach,
                    "booking_cost": booking_cost,
                    "date_human_readable": date_human_readable,
                })
    
    context = {
        "booking_items": booking_items,
        "total_booking_amount": total_booking_amount,
        "number_of_bookings": number_of_bookings
    }
    
    return context