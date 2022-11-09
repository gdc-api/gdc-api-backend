from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = "/api/users/"
        cls.login_url = "/api/login/"
        cls.update_url = "/api/users/"

        cls.user_adm = {
            "email": "adm@adm.com",
            "password": "aoskj012983018gj",
            "first_name": "Adm",
            "last_name": "Super"
        }

        cls.user = {
            "email": "jose@email.com",
            "password": "asdas98012893",
            "first_name": "Jose",
            "last_name": "Duarte",
   
        }

        cls.user_not_owner = {
            "email": "notowner@email.com",
            "password": "asdas98012893",
            "first_name": "Not",
            "last_name": "Owner",
   
        }


        cls.user_login = {
            "email": "jose@email.com",
            "password": "asdas98012893"
        }

        cls.adm_login = {
            "email": "adm@adm.com",
            "password": "aoskj012983018gj"
        }


    def test_create_user(self):
        response = self.client.post(self.register_url, data=self.user)
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)

    def test_create_user_wrong_keys(self):
        response = self.client.post(self.register_url, data={})
        
        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(response.data["first_name"][0], "This field is required.")
        self.assertEqual(response.data["last_name"][0], "This field is required.")
        self.assertEqual(response.data["email"][0], "This field is required.")
        self.assertEqual(response.data["password"][0], "This field is required.")

    def test_login_user(self):
        self.client.post(self.register_url, self.user, format="json")
        login = self.client.post(self.login_url, self.user_login, format="json")
        expected_status_code = status.HTTP_200_OK
        result_status_code = login.status_code
        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn("token", login.data)


    def test_login_without_keys(self):
        self.client.post(self.register_url, self.user)
        login = self.client.post(self.login_url, data={})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = login.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(login.data["email"][0], "This field is required.")
        self.assertEqual(login.data["password"][0], "This field is required.")

    def test_admin_list_users(self):
        self.client.post(self.register_url, self.user_adm, format="json")
        login = self.client.post(self.login_url, self.adm_login, format="json")
        expected_status_code = status.HTTP_200_OK
        result_status_code = login.status_code
        self.assertEqual(expected_status_code, result_status_code)

    def test_update_by_not_owner(self):
        user_owner = User.objects.create_user(**self.user)
        token_owner = Token.objects.create(user=user_owner)
        not_owner = User.objects.create_user(**self.user_not_owner)
        token_not_owner = Token.objects.create(user=not_owner)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_not_owner.key)
        response = self.client.patch(f'{self.update_url}{user_owner.id}/', data={"last_name": "Not owner PATCH"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_by_owner(self):
        user_owner = User.objects.create_user(**self.user)
        token = Token.objects.create(user=user_owner)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.patch(f'{self.update_url}{user_owner.id}/', data={"last_name": "Owner PATCH"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      
    def test_user_cant_list_users(self):
        user = User.objects.create_user(**self.user_adm)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(self.register_url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_list_users(self):
        admin = User.objects.create_superuser(**self.user_adm)
        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(self.register_url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
