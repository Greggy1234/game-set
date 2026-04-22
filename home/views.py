from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib import messages
from .forms import FeedbackForm

# Create your views here.

def index(request):
    """A view to return the index page"""    
    feedback_form = FeedbackForm()
    
    return render(
        request, 
        'home/index.html',
        {
            "feedback_form": feedback_form,
        }
    )


def add_feedback(request):
    if request.method == "POST":
        feedback_form = FeedbackForm(data=request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            messages.success(request, 'Thank you for your feedback. We will review within 48 hours!')
        else:
            messages.error(request, 'Something went wrong, please try to submit the form again')
    
    return HttpResponseRedirect(reverse('home'))