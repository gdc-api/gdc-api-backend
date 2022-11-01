from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from models import User


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
            "f_name": "Jose",
            "l_name": "Duarte",
            "phone": "1112345678",
        }

        cls.user_not_owner = {
            "email": "notowner@email.com",
            "password": "asdas98012893",
            "f_name": "Not",
            "l_name": "Owner",
            "phone": "1112345678",
        }


        cls.user_login = {
            "email": "jose@email.com",
            "password": "asdas98012893"
        }

        cls.adm_login = {
            "email": "adm@adm.com",
            "password": "aoskj012983018gj"
        }


        """ user
        f_name
        l_name
        phone
        email - pk
        sobre / bio
        password
         """
    def test_create_user(self):
        response = self.client.post(self.register_url, data=self.user)
        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)

    def test_create_user_wrong_keys(self):
        response = self.client.post(self.register_url, data={})
        
        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(response.data["f_name"][0], "This field is required.")
        self.assertEqual(response.data["l_name"][0], "This field is required.")
        self.assertEqual(response.data["phone"][0], "This field is required.")
        self.assertEqual(response.data["email"][0], "This field is required.")
        self.assertEqual(response.data["sobre"][0], "This field is required.")
        self.assertEqual(response.data["password"][0], "This field is required.")

    def test_login_user(self):
        response = self.client.post(self.register_url, self.user)
        response = self.client.post(self.login_url, self.user_login)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn("token", response.data)


    def test_login_wrong_keys(self):
        response = self.client.post(self.register_url, self.user)
        response = self.client.post(self.login_url, data={})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(response.data["email"][0], "This field is required.")
        self.assertEqual(response.data["password"][0], "This field is required.")

    def test_admin_list_users(self):#verificar
        response = self.client.post(self.register_url, self.user_adm)
        response = self.client.post(self.login_url, self.adm_login)
        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)

    def test_update_by_not_owner(self):
        user_owner = User.objects.create_user(**self.user)
        token_owner = Token.objects.create(user=user_owner)
        not_owner = User.objects.create_user(**self.user_not_owner)
        token_not_owner = Token.objects.create(user=not_owner)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_not_owner.key)
        response = self.client.patch(f'{self.update_url}{user_owner.id}/', data={"l_name": "Not owner PATCH"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_by_owner(self):
        user_owner = User.objects.create_user(**self.user)
        token = Token.objects.create(user=user_owner)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.patch(f'{self.update_url}{user_owner.id}/', data={"l_name": "Owner PATCH"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_is_active_with_not_adm(self):
        user = User.objects.create_user(**self.user)
        token = Token.objects.create(user=user)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f'{self.update_url}{user.id}/management/', data={"is_active": False})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_is_active_with_adm(self):
        adm = User.objects.create_superuser(**self.user_adm)
        token = Token.objects.create(user=adm)

        user_seller = User.objects.create_user(**self.user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        deactive_user = {"is_active": False}

        response = self.client.patch(
            f'{self.update_url}{user_seller.id}/management/', data=deactive_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_active"],
                         deactive_user["is_active"])
