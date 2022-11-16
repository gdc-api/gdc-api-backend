from datetime import datetime

import pytz
from django.core.management.base import BaseCommand
from interviews.models import Interview

utc = pytz.UTC


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = utc.localize(datetime.now())

        interviews = Interview.objects.all()

        for i in interviews:
            if i.schedule < now:
                i.passed = True
                i.save()

        ...
