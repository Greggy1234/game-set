from django.test import TestCase
from .forms import FeedbackForm


# Test for the feedback form
class TestFeedbackForm(TestCase):
    def test_form_is_valid(self):
        """ Test for all fields """
        form = FeedbackForm({
            'name': 'Greg Reid',
            'email' : 'asdksajl@googmeail.com',
            'message': 'I want to add friends'
        })
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_form_is_not_valid_name(self):
        """ Test for no name """
        form = FeedbackForm({
            'name': '',
            'email' : 'asdksajl@googmeail.com',
            'message': 'I want to add friends'
        })
        self.assertFalse(form.is_valid(), msg="No name field given in test")
    
    def test_form_is_not_valid_email(self):
        """ Test for no name """
        form = FeedbackForm({
            'name': 'Greg Reid',
            'email' : '',
            'message': 'I want to add friends'
        })
        self.assertFalse(form.is_valid(), msg="No email field given in test")

    def test_form_is_not_valid_message(self):
        """ Test for no message """
        form = FeedbackForm({
            'name': 'Greg Reid',
            'email' : 'asdksajl@googmeail.com',
            'message': ''
        })
        self.assertFalse(form.is_valid(), msg="No message field given in test")