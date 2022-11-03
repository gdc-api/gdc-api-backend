from django.test import TestCase
from django.db import IntegrityError

from applications.models import Application

from ..models import User
from companies.models import Comapany
from jobs.models import Job


class TestUserModelAndRelation(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        # user creation
        cls.user_data = {
            "first_name": "Fernando",
            "last_name": "Scramignon",
            "phone": 21964174844,
            "email": "scramignonnarde@gmail.com",
            "bio": "blablabla",
            "password": "1234",
            "github": "git",
            "linkedin": "link",
        }

        cls.user_data_wrong_names = {
            **cls.user_data,
            "first_name": 4566456,
            "last_name": 45365453,
        }

        cls.user_data_wrong_email = {**cls.user_data, "email": 2354153}

        cls.user_data_wrong_social = {
            **cls.user_data,
            "linkedin": 48646,
            "github": 156561,
        }

        cls.user = User.models.create_user(**cls.user_data)

        # To create an application for the relations test you need company and job

        # comapany creation
        cls.company_data = {
            "name": "kenzie",
            "description": "best company",
            "segment": "tech",
        }

        cls.company = Comapany.objects.create(**cls.company_data)

        # job creation
        cls.job_data = {
            "url": "url_string",
            "title": "some_title",
            "level": "level_up",
            "category": "category1",
            "period": "part_time",
            "estimated_pay": 3000,
            "location": "cool_building",
            "contract": "millionaire",
            "company": cls.company,
        }

        cls.job_data_2 = {**cls.job_data, "title": "some_title_2"}

        cls.job = Job.objects.create(**cls.job_data)
        cls.job_2 = Job.objects.create(**cls.job_data_2)

        # application creation
        cls.application_data = {"user": cls.user, "job": cls.job}
        cls.application_data_2 = {"user": cls.user, "job": cls.job_2}

        cls.application = Application.objects.create(**cls.application_data)
        cls.application_2 = Application.objects.create(**cls.application_data_2)

    def test_user_fields(self):
        """
        checks if user was created correctly
        """
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.phone, self.user_data["phone"])
        self.assertEqual(self.user.bio, self.user_data["bio"])
        self.assertEqual(self.user.github, self.user_data["github"])
        self.assertEqual(self.user.linkedin, self.user_data["linkedin"])

    def test_phone_is_nullable(self):
        """
        checks if phone number is an optional field
        """

        nullable = self.user._meta.get_field("phone").null
        blankable = self.user._meta.get_field("phone").blank
        self.assertTrue(nullable)
        self.assertTrue(blankable)

    def test_github_is_nullable(self):
        """
        checks if github is an optional field
        """

        nullable = self.user._meta.get_field("github").null
        blankable = self.user._meta.get_field("github").blank
        self.assertTrue(nullable)
        self.assertTrue(blankable)

    def test_bio_is_nullable(self):
        """
        checks if bio is an optional field
        """

        nullable = self.user._meta.get_field("bio").null
        blankable = self.user._meta.get_field("bio").blank
        self.assertTrue(nullable)
        self.assertTrue(blankable)

    def test_not_null_fields(self):
        """
        checks properties that can't be null
        """

        is_first_name_nullable = self.user._meta.get_field("first_name").null
        is_last_name_nullable = self.user._meta.get_field("last_name").null
        is_email_nullable = self.user._meta.get_field("email").null
        is_password_nullable = self.user._meta.get_field("password").null

        self.assertFalse(is_first_name_nullable)
        self.assertFalse(is_last_name_nullable)
        self.assertFalse(is_email_nullable)
        self.assertFalse(is_password_nullable)

    def test_user_creation_wrong_format(self):
        """
        checks if wrong format raises exception
        """
        with self.assertRaises(IntegrityError):
            User.objects.create(self.user_data_wrong_names)

        with self.assertRaises(IntegrityError):
            User.objects.create(self.user_data_wrong_email)

        with self.assertRaises(IntegrityError):
            User.objects.create(self.user_data_wrong_social)

    def test_user_can_have_multiple_applications(self):
        """
        checks if user can have multiple applications
        """
        self.assertEqual(self.user.applications.values()[0]["id"], self.application.id)
        self.assertEqual(
            self.user.applications.values()[1]["id"], self.application_2.id
        )
