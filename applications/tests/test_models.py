from django.db import IntegrityError
from django.test import TestCase

from ..models import Application
from users.models import User
from jobs.models import Job
from interviews.models import Interview

from companies.models import Company

from datetime import datetime


class TestApplicationModelAndRelations(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # before createing a application i need a user and a job

        # Job creation:
        # To create a job a need a company
        cls.company_data = {
            "name": "kenzie",
            "description": "Best company in the world!",
            "segment": "tech",
        }

        cls.company = Company.objects.create(**cls.company_data)

        cls.job_data = {
            "url": "www.url.com",
            "title": "developer",
            "level": "Júnior",
            "category": "Front-End",
            "period": "full time",
            "estimated_pay": 3000,
            "location": "cool building",
            "contract": "pj",
            "company": cls.company,
        }

        cls.job_data_2 = {**cls.job_data, "level": "Pleno", "category": "Back-End", "url": "www.url_2.com"}

        cls.job = Job.objects.create(**cls.job_data)
        cls.job_2 = Job.objects.create(**cls.job_data_2)

        # user creation
        cls.user_data = {
            "first_name": "Fernando",
            "last_name": "Scramignon",
            "username":"fernando@email.com",
            "email": "fernando@email.com",
            "bio": "A cool storie",
            "password": "1234",
        }

        cls.user_data_2 = {**cls.user_data, "email": "wrong@email.com", "username":"fernando2"}

        cls.user = User.objects.create_user(**cls.user_data)
        cls.user_2 = User.objects.create_user(**cls.user_data_2)

        # application creation
        cls.application_data = {"user": cls.user, "job": cls.job}

        cls.application = Application.objects.create(**cls.application_data)

        # second user in the same job
        cls.application_data_2 = {"user": cls.user_2, "job": cls.job}

        # data for testing creations with wrong format
        cls.application_data_wrong_format = {"user": None, "job": "cookie"}

        # creates interview
        cls.interview_data = {
            "schedule": datetime(2023, 1, 1),
            "location": "wallstreet",
            "application": cls.application,
        }

        # cls.interview = Interview.objects.create(**cls.interview_data)

        # cls.interview_data_2 = {
        #     "schedule": datetime(2023, 2, 2),
        #     "location": "timesquare",
        #     "application": cls.application,
        # }

    def test_application_fields(self):
        """
        checks if creation was successfull
        """

        self.assertTrue(self.application.created_at)
        self.assertTrue(self.application.is_active)
        self.assertEqual(self.application.user.email, self.user.email)
        self.assertEqual(self.application.job.title, self.job.title)

    def test_creation_with_wrong_format(self):
        """
        checks if exception is raised when wrong format is passed to an application
        """

        with self.assertRaises(ValueError):
            Application.objects.create(**self.application_data_wrong_format)

    def test_job_can_have_multiple_applications(self):
        """
        checks if one user can apply to multiple jobs
        """

        Application.objects.create(**self.application_data_2)
        # the first relation is already created on the set up
        self.assertEqual(self.job.applications.count(), 2)

    def test_application_can_only_be_in_one_job(self):
        """
        checks if after adding application to job 1 and to job 2,
        the application job changes instead of just adding one more relation
        """

        self.job_2.applications.add(self.application)
        self.job_2.save()

        self.assertEqual(self.application.job.id, self.job_2.id)

    def test_user_can_have_multiple_applications(self):
        application_data = {"user": self.user, "job": self.job}
        Application.objects.create(**application_data)

        self.assertEqual(self.user.applications.count(), 2)

    def test_application_can_only_have_one_user(self):
        """
        checks if after adding the same application to user 1 and to user 2,
        the application user changes instead of just adding one more relation (or breaking)
        """
        self.user_2.applications.add(self.application)
        self.user_2.save()

        self.assertEqual(self.application.user.id, self.user_2.id)

    # def test_application_can_have_multiple_interviews(self):
    #     """
    #     checks if one application can have multiple interviews
    #     """
    #     Interview.objects.create(**self.interview_data_2)
    #     self.assertEqual(self.application.interviews.count(), 2)

    # def test_interview_can_only_have_one_application(self):
    #     """
    #     checks if after adding the same interview to application 1 and to application 2,
    #     the interview application changes instead of just adding one more relation (or breaking)
    #     """

    #     application_2 = Application.objects.create(**self.application_data_2)
    #     application_2.interviews.add(self.interview)
    #     application_2.save()

    #     self.assertEqual(self.interview.application.id, application_2.id)
