from django.test import TestCase

from ..models import Job
from companies.models import Company


class JobModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.job_data = {
            "url": "https://example-url.com",
            "title": "Node.js Developer",
            "level": "Sênior",
            "category": "Full-Stack",
            "period": "40hrs/Week",
            "estimated_pay": 5000,
            "location": "Remote",
            "contract": "CLT",
        }

        cls.company_data = {
            "name": "SauCom",
            "description": "Empresa na área da saúde",
            "segment": "Saúde"
        }

        cls.company = Company.objects.create(**cls.company_data)
        cls.job = Job.objects.create(**cls.job_data, company=cls.company,)

    def test_field_rules(self):
        """
        tests the rules of the fields.
        """

        url_max_length = self.job._meta.get_field("url").max_length
        title_max_length = self.job._meta.get_field("title").max_length
        level_max_length = self.job._meta.get_field("level").max_length
        category_max_length = self.job._meta.get_field(
            "category").max_length
        period_max_length = self.job._meta.get_field("period").max_length
        location_max_length = self.job._meta.get_field(
            "location").max_length
        contract_max_length = self.job._meta.get_field(
            "contract").max_length

        url_is_unique = self.job._meta.get_field("url").unique

        msg = "Check if the {} field {} attribute was set to: {}"

        self.assertEqual(url_max_length, 254,
                         msg.format("url", "max_length", 254))

        self.assertEqual(title_max_length, 127,
                         msg.format("title", "max_length", 127))

        self.assertEqual(level_max_length, 15,
                         msg.format("level", "max_length", 15))

        self.assertEqual(category_max_length, 15,
                         msg.format("category", "max_length", 15))

        self.assertEqual(period_max_length, 15,
                         msg.format("period", "max_length", 15))

        self.assertEqual(location_max_length, 30,
                         msg.format("location", "max_length", 30))

        self.assertEqual(contract_max_length, 15,
                         msg.format("contract", "max_length", 15))

        self.assertTrue(url_is_unique,
                        msg.format("url", "unique", True))

        ...

    def test_job_fields(self):
        """
        tests model saved attributes.
        """

        msg = "The {} field value is different from the expected: {}"

        self.assertEqual(self.job.url, self.job_data['url'],
                         msg.format("url", self.job_data['url']))

        self.assertEqual(self.job.title, self.job_data['title'],
                         msg.format("title", self.job_data['title']))

        self.assertEqual(self.job.period, self.job_data['period'],
                         msg.format("period", self.job_data['period']))

        self.assertEqual(self.job.estimated_pay, self.job_data['estimated_pay'],
                         msg.format("estimated_pay", self.job_data['estimated_pay']))

        self.assertEqual(self.job.location, self.job_data['location'],
                         msg.format("location", self.job_data['location']))

        self.assertEqual(self.job.contract, self.job_data['contract'],
                         msg.format("contract", self.job_data['contract']))

        ...
