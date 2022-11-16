
from django.test import TestCase
from model_bakery import baker
from django.db import IntegrityError


class CompaniesTestModel(TestCase):
    @classmethod
    def setUp(cls):
        cls.response = baker.make_recipe('companies.generic_valid_company')

    def test_creating_a_company_with_valid_data(self):
        company = baker.make_recipe('companies.valid_company')

        self.assertTrue(company.id)

        self.assertEqual(company.name, 'Kenzie Store')

        self.assertEqual(company.description, 'The ideal store for devs')

        self.assertEqual(company.segment, 'Information Technology')

    def test_valid_id_field(self):
        id_field_length = self.response.id

        self.assertEqual(len(str(id_field_length)), 36)

    def test_cannot_create_a_new_company_with_a_duplicated_name(self):
        with self.assertRaises(IntegrityError):
            baker.make_recipe('companies.generic_valid_company')

    def test_name_field_must_have_max_length_defined(self):
        max_length = self.response._meta.get_field("name").max_length

        self.assertEqual(max_length, 50)

    def test_name_field_must_unique_property_defined(self):
        is_unique = self.response._meta.get_field("name").unique

        self.assertEqual(is_unique, True)

    def test_name_field_must_not_be_null_or_blank(self):
        is_null = self.response._meta.get_field("name").null
        is_blank = self.response._meta.get_field("name").blank

        self.assertEqual(is_null, False)
        self.assertEqual(is_blank, False)

        with self.assertRaises(IntegrityError):
            baker.make_recipe('companies.invalid_company_name')

    def test_description_field_must_not_have_a_max_length_defined(self):
        max_length = self.response._meta.get_field("description").max_length

        self.assertEqual(max_length, None)

    def test_segment_field_must_have_max_length_defined(self):
        max_length = self.response._meta.get_field("segment").max_length

        self.assertEqual(max_length, 30)

    def test_segment_field_must_not_be_null_or_blank(self):
        is_null = self.response._meta.get_field("segment").null
        is_blank = self.response._meta.get_field("segment").blank

        self.assertEqual(is_null, False)
        self.assertEqual(is_blank, False)

        with self.assertRaises(IntegrityError):
            baker.make_recipe('companies.invalid_company_segment')
