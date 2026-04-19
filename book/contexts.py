from django.shortcuts import get_object_or_404
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
            for time, info in times.items():
                booking_time = time
                coach_id = info["coach"]
                booking_cost = int(info["cost"])
                total_booking_amount += int(info["cost"])
                booking_coach = None
                if coach_id:
                    booking_coach = get_object_or_404(Coach, id=coach_id)
                number_of_bookings += 1
                booking_items.append({
                    "court": court,
                    "booking_date": booking_date,
                    "booking_time": booking_time,
                    "booking_coach": booking_coach,
                    "booking_cost": booking_cost
                })
    
    context = {
        "booking_items": booking_items,
        "total_booking_amount": total_booking_amount,
        "number_of_bookings": number_of_bookings
    }
    
    return context