from rest_framework.test import APITestCase

from users.models import User

import ipdb

class ApplicationViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "first_name": "Fernando",
            "last_name": "Scramignon",
            "email": "fernando@email.com",
            "password": "1234",
        }

        cls.user_login_data = {
            "username":cls.user_data["email"],
            "password":cls.user_data["password"]
        }

        cls.user = User.objects.create_user(**cls.user_data, username=cls.user_data["email"])

        cls.job_data = {
            "url": "www.url.com",
            "title": "developer",
            "level": "Júnior",
            "category": "Front-End",
            "period": "full time",
            "estimated_pay": 3000,
            "location": "cool building",
            "contract": "pj",
            "company": {
            "name": "kenzie",
            "description": "Best company in the world!",
            "segment": "tech",
        },
        }

        cls.list_create_url = "/api/applications/"
        cls.login_url = "/api/login/"
    
    def test_application_creation(self):
        token = self.client.post(self.login_url, self.user_login_data, format="json").data["token"]
        response = self.client.post(
            self.list_create_url,
            {   
                "job":self.job_data
            },
            HTTP_AUTHORIZATION=f"Token {token}",
            format="json"
        )
        
        self.assertEqual(self.user.email, self.user.username)

    def test_application_listing(self):
        token = self.client.post(self.login_url, self.user_login_data, format="json").data["token"]

        response = self.client.get(
            self.list_create_url,
            HTTP_AUTHORIZATION=f"Token {token}",
            format="json"
        )

        self.assertEqual(len(response.data["results"]), 0)