import os
from datetime import datetime, timedelta

import dotenv
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from interviews.models import Interview

dotenv.load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        to_send = {}
        interviews = Interview.objects.all()
        now = datetime.now().date()

        for i in interviews:
            if i.schedule.date() + timedelta(days=1) == now:
                if i.user.email in to_send.keys():
                    to_send[i.user.email].append(i.application)

        ...
