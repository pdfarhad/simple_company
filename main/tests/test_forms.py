from django.test import TestCase
from django.core import mail
from main import forms
from django.urls import reverse


class TestForm(TestCase):

    def test_valid_contact_us_form_send_emails(self):

        form = forms.ContactForm({
            'name':"pd",
            'message':"I love you pakhi"
        })
        self.assertTrue(form.is_valid())
        with self.assertLogs('main.forms', level="INFO") as cm:
            form.send_mail()
            self.assertEqual(len(mail.outbox),1)
            self.assertEqual(mail.outbox[0].subject,"Site message")
            self.assertGreaterEqual(len(cm.output),1)
    
    def test_invalid_contact_us_form(self):
        form = forms.ContactForm({
            'message': "Hello bhai"

        })
        self.assertFalse(form.is_valid())

    def test_contact_us_page_works(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response='main/contact_form.html')
        self.assertContains(response,'BookTime')
        self.assertIsInstance(response.context["form"],forms.ContactForm)