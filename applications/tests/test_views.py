from rest_framework.test import APITestCase

import ipdb


class ApplicationViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user_data = {
            "email": "john@mail.com",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe"
        }

        cls.other_user_data = {
            "email": "doe@mail.com",
            "password": "1234",
            "first_name": "doe",
            "last_name": "jhon"
        }

        cls.other_user_login_data = {
            "email": cls.other_user_data["email"],
            "password": cls.other_user_data["password"]
        }

        cls.user_login_data = {
            "email": cls.user_data["email"],
            "password": cls.user_data["password"]
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

        cls.other_application = {
            "job": {
                "url": "www.url3.com",
                "title": "developer frontend",
                "period": "half time",
                "location": "home",
                "contract": "pj",
                "estimated_pay": 9000,
                "company": {
                    "name": "Kenzie2",
                    "description": "company",
                    "segment": "tech"
                }
            }
        }

        cls.duplicated_company = {
            "job": {
                "url": "www.url2.com",
                "title": "developer fullstack",
                "period": "half time",
                "location": "home",
                "contract": "pj",
                "estimated_pay": 5000,
                "company": {
                    "name": "Kenzie1",
                    "description": "best company",
                    "segment": "tech"
                }
            }
        }

        cls.application_without_key_job = {
            "url": "www.url4.com",
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

        cls.job_without_company = {
            "job": {
                "url": "www.url5.com",
                "title": "developer",
                "period": "half time",
                "location": "home",
                "contract": "pj",
                "estimated_pay": 3000
            }
        }

        cls.list_create_url = "/api/applications/"
        cls.create_user_url = "/api/users/"
        cls.login_url = "/api/login/"

    def test_must_be_a_possible_to_register_a_new_application(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        response = self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        self.assertIn("user", response.json())
        self.assertIn("job", response.json())
        self.assertIn("company", response.json()['job'])

    def test_should_not_be_possible_to_create_without_authentication(self):
        response = self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_the_job_key_must_be_mandatory(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        response = self.client.post(
            self.list_create_url,
            self.application_without_key_job,
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_the_company_key_must_be_mandatory(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        response = self.client.post(
            self.list_create_url,
            self.job_without_company,
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_shouldnt_be_possible_to_use_the_same_url_two_or_more_times(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        response = self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_it_should_not_be_possible_to_duplicate_the_company_name(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        response = self.client.post(
            self.list_create_url,
            self.duplicated_company,
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_the_user_should_be_able_to_list_their_applications(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        response = self.client.get(
            self.list_create_url,
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("count", response.json())
        self.assertIn("next", response.json())
        self.assertIn("count", response.json())
        self.assertIn("results", response.json())

    def test_the_user_must_be_authenticated_to_list_their_applications(self):
        response = self.client.get(
            self.list_create_url,
            format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_the_user_must_have_access_to_only_their_applications(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        self.client.post(
            self.create_user_url,
            self.other_user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        other_user_login = self.client.post(
            self.login_url,
            self.other_user_login_data,
            format="json"
        )

        token = login.json()['token']
        other_user_token = other_user_login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {other_user_token}"
        )

        self.client.post(
            self.list_create_url,
            self.other_application,
            format="json"
        )

        response = self.client.get(
            self.list_create_url,
            format="json"
        )

        results = response.json()['results']

        self.assertEqual(len(results), 1)

    def test_creating_application_referencing_company_id(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        application = self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        company_id = application.json()['job']['company']['id']

        response = self.client.post(
            f"/api/applications/company/{company_id}/",
            self.job_without_company,
            format="json"
        )

        self.assertIn("user", response.json())
        self.assertIn("job", response.json())
        self.assertIn("company", response.json()['job'])

    def test_creating_application_referencing_duplicated_company_id(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        application = self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        company_id = application.json()['job']['company']['id']

        self.client.post(
            f"/api/applications/company/{company_id}/",
            self.job_without_company,
            format="json"
        )

        response = self.client.post(
            f"/api/applications/company/{company_id}/",
            self.job_without_company,
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_creating_app_referencing_company_id_without_authentication(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        application = self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        company_id = application.json()['job']['company']['id']

        self.client.credentials(
            HTTP_AUTHORIZATION=""
        )

        response = self.client.post(
            f"/api/applications/company/{company_id}/",
            self.job_without_company,
            format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_it_should_be_possible_to_soft_delete(self):

        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        application = self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        application_id = application.json()['id']

        response = self.client.delete(
            f"/api/applications/{application_id}/",
        )
        app = self.client.get(
            "/api/applications/",
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(app.json()['results'][0]['is_active'], False)

    def test_should_not_delete_an_inactive_application(self):
        self.client.post(
            self.create_user_url,
            self.user_data,
            format="json"
        )

        login = self.client.post(
            self.login_url,
            self.user_login_data,
            format="json"
        )

        token = login.json()['token']

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        application = self.client.post(
            self.list_create_url,
            self.application,
            format="json"
        )

        application_id = application.json()['id']

        self.client.delete(
            f"/api/applications/{application_id}/",
        )

        response = self.client.delete(
            f"/api/applications/{application_id}/",
        )

        self.assertEqual(response.status_code, 406)
