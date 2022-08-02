from django.test import TestCase
from django.contrib.auth.models import User
from Company.models import Company
from ..models import AccessPermission
from ..acl import Acl
from ..exceptions import AclDenied


class AclTest(TestCase):
    fixtures = ['fixtures/dump.json']

    def setUp(self) -> None:
        self.user_a = User.objects.get(username='userA')
        self.user_b = User.objects.get(username='userB')
        self.company_a = Company.objects.get(name='Company A')
        self.company_b = Company.objects.get(name='Company B')
        self.permission_create = AccessPermission.objects.get(slug='create', module__slug='customer')
        self.permission_read = AccessPermission.objects.get(slug='read', module__slug='customer')

    def test_check_acl(self):
        acl_a = Acl(self.user_a)
        self.assertTrue(acl_a.check('customer', 'create'))
        self.assertTrue(acl_a.check('customer', 'create', self.company_a))
        self.assertFalse(acl_a.check('customer', 'create', self.company_b))

    def test_check_attr(self):
        acl_a = Acl(self.user_a)

        self.assertTrue(acl_a.has_customer_create)
        self.assertFalse(acl_a.has_company_create)

    def test_check_raise(self):
        acl_a = Acl(self.user_a)

        with self.assertRaises(AclDenied):
            acl_a.check_raise('customer', 'create', self.company_b)

        acl_a.check_raise('customer', 'create', self.company_a)
