from django.test import TestCase
from django.contrib.auth.models import User

from Company.models import Company
from ..models import AccessPermission


class AccessPermissionTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self) -> None:
        self.user_a = User.objects.get(username='userA')
        self.user_b = User.objects.get(username='userB')
        self.company_a = Company.objects.get(name='Company A')
        self.company_b = Company.objects.get(name='Company B')
        self.permission_create = AccessPermission.objects.get(slug='create', module__slug='customer')
        self.permission_read = AccessPermission.objects.get(slug='read', module__slug='customer')

    def test_has_access_no_company(self):
        """
        Test method without passing company
        """
        self.assertTrue(self.permission_create.has_access(self.user_a))
        self.assertTrue(self.permission_create.has_access(self.user_b))

    def test_has_access_with_company(self):
        """
        Test method with passing company
        """
        self.assertTrue(self.permission_create.has_access(self.user_a, self.company_a))
        self.assertFalse(self.permission_create.has_access(self.user_a, self.company_b))

        self.assertTrue(self.permission_create.has_access(self.user_b, self.company_b))
        self.assertFalse(self.permission_create.has_access(self.user_b, self.company_a))

    def test_get_companies(self):
        self.assertEqual(self.permission_create.get_companies(self.user_a), [self.company_a])
        self.assertEqual(self.permission_create.get_companies(self.user_b), [self.company_b])

        self.assertSetEqual(set(self.permission_read.get_companies(self.user_a)), {self.company_a, self.company_b})
        self.assertSetEqual(set(self.permission_read.get_companies(self.user_b)), {self.company_a, self.company_b})


    def test_get_companies_flat(self):
        self.assertEqual(self.permission_create.get_companies(self.user_a, flat=True), [self.company_a.id])
        self.assertEqual(self.permission_create.get_companies(self.user_b, flat=True), [self.company_b.id])
