from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from shared.views import prep_field
from djqscsv import render_to_csv_response
from django.core.mail import EmailMessage
from authentication.models import User
import io, csv
from celery.decorators import task
from time import sleep



# for working in terminal
# celery -A myproject worker -l info --pool=solo


@shared_task
def download_as_csv_task(user_email, user_id_list):
    queryset = User.objects.filter(pk__in = user_id_list)
    print(queryset)

    field_names = {
        "id" : "User ID",
        "username":"Username",
        "first_name" : "First Name",
        "last_name" : "Last name",
        'email' : "Email",
    }
    csv_file =  io.StringIO()

    writer = csv.writer(csv_file)
    writer.writerow(field_names.values())
    for obj in queryset:
        writer.writerow([prep_field(obj, field) for field in field_names.keys()])

    email = EmailMessage(
        'Subject',
        'Testing CSV',
        None,
        [user_email],
        attachments = [
            ('data.csv', csv_file.getvalue(), 'text/csv'),
        ],
    )
    email.send()
    return f"worked suffesfully"


@shared_task
def sum(a,b):
    return a+b


@shared_task
def test(a):
    sleep(a)
    return f'slept'

@shared_task
def test2(a):
    for i in range(100000):
        print(i)
    return f'slept'

