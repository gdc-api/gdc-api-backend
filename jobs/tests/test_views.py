from rest_framework import APITestCase
import json


class JobsTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = {
            "email": "john@mail.com",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe"
        }

        cls.login = {
            "email": "john@mail.com",
            "password": "1234",
        }

        cls.application = {
            "job": {
                "url": "www.url1.com",
                "title": "developer",
                "period": "half time",
                "location": "home",
                "contract": "pj",
                "estimated_pay": 3000,
                "company": {
                    "name": "Kenzie1",
                    "description": "best company",
                    "segment": "tech"
                }
            }
        }

        cls.job_update_title = {
            "title": "has been updated"
        }

        cls.job_update_id = {
            "id": "should not be updated"
        }

        cls.create_user_url = "/api/users/"
        cls.login_url = "/api/login/"
        
        cls.create_aplication_url = "/api/applications/"
        cls.update_job_url ="/api/jobs/"


    def test_jobs_update_any_field(self):
        self.client.post(
            self.create_user_url,
            self.user,
            format='json'
        )
        
        login = self.client.post(
            self.login_url,
            self.login,
            format='json'
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        application = self.client.post(
            self.create_aplication_url,
            self.application,
            format='json'
        )

        job = application.json()['job']
        job_id = job['id']

        response = self.client.patch(
            f'{self.update_job_url}{job_id}/',
            self.job_update_title,
            format='json'
        )

        self.assertEqual(response.json()['title'], self.update_title['title'])
        self.assertEqual(response.json()['location'], job['location'])

    def test_jobs_cant_update_without_authorization(self):
        self.client.post(
            self.create_user_url,
            self.user,
            format='json'
        )

        response = self.client.post(
            self.create_aplication_url,
            self.application,
            format='json'
        )

        self.assertEqual(response.status_code, 401)
    
    def test_jobs_cant_update_id(self):
        self.client.post(
            self.create_user_url,
            self.user,
            format='json'
        )
        
        login = self.client.post(
            self.login_url,
            self.login,
            format='json'
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        application = self.client.post(
            self.create_aplication_url,
            self.application,
            format='json'
        )

        job = application.json()['job']
        job_id = job['id']

        response = self.client.patch(
            f'{self.update_job_url}{job_id}/',
            self.job_update_id,
            format='json'
        )

        self.assertNotEqual(response.json()['id'], self.update_id['id'])
        self.assertEqual(response.json()['id'], response.json()['id'])