from rest_framework.test import APITestCase
import json


class CompanyTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
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

        cls.update_name = {
            "name": "updated"
        }

        cls.update_id = {
            "id": "should not be updated"
        }

    def test_it_should_be_possible_to_update_any_field(self):

        self.client.post(
            '/api/users/',
            self.user,
            format='json'
        )

        token = self.client.post(
            '/api/login/',
            self.login,
            format='json'
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.json()['token']}"
        )

        application = self.client.post(
            '/api/applications/',
            self.application,
            format='json'
        )

        company = application.json()['job']['company']
        company_id = company['id']

        response = self.client.patch(
            f'/api/companies/{company_id}/',
            self.update_name,
            format='json'
        )

        self.assertEqual(response.json()['name'], self.update_name['name'])
        self.assertEqual(
            response.json()['description'],
            company['description']
        )

    def test_should_not_be_possible_to_update_without_authentication(self):

        self.client.post(
            '/api/users/',
            self.user,
            format='json'
        )

        response = self.client.post(
            '/api/applications/',
            self.application,
            format='json'
        )

        self.assertEqual(response.status_code, 401)

    def test_it_should_not_be_possible_to_update_the_company_id(self):

        self.client.post(
            '/api/users/',
            self.user,
            format='json'
        )

        token = self.client.post(
            '/api/login/',
            self.login,
            format='json'
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.json()['token']}"
        )

        application = self.client.post(
            '/api/applications/',
            self.application,
            format='json'
        )

        company = application.json()['job']['company']
        company_id = company['id']

        response = self.client.patch(
            f'/api/companies/{company_id}/',
            self.update_id,
            format='json'
        )

        self.assertNotEqual(response.json()['id'], self.update_id['id'])
        self.assertEqual(
            response.json()['id'],
            response.json()['id']
        )
