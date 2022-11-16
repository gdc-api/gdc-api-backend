import os
from datetime import datetime, timedelta

import dotenv
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from interviews.models import Interview


dotenv.load_dotenv()


class Command(BaseCommand):
    def verify_schedules() -> dict:
        interviews = Interview.objects.all()
        now = datetime.now().date()
        send_to = {}

        for i in interviews:
            if not i.passed and i.schedule.date() - timedelta(days=1) == now:
                interview = {
                    "application": i.application,
                    "schedule": i.schedule,
                }

                if i.user.email in send_to.keys():
                    send_to[i.user.email].append(interview)
                else:
                    send_to[i.user.email] = [interview]

        return send_to
        ...

    def build_messages(send_to: dict) -> dict:
        messages = {}

        for u, u_interviews in send_to.items():
            for i in u_interviews:
                message = f"Entrevista para {i['application'].job.company.name} amanhã às: {i['schedule'].time()} "

                if u in messages.keys():
                    messages[u].append(message)
                else:
                    messages[u] = [message]

        return messages
        ...

    def send_emails(messages):

        for u, u_messages in messages.items():

            email_message = "\n".join(u_messages)

            send_mail(
                subject="Lembrete de entrevista(s)",
                message=email_message,
                from_email=os.getenv("EMAIL_HOST_USER"),
                recipient_list=[u],
                fail_silently=False,
            )
        ...

    def handle(self, *args, **kwargs):

        send_to = self.verify_schedules()

        messages = self.build_messages(send_to)

        self.send_emails(messages)

        ...
