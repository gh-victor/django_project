from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

test_email1='test1@sample.com'
test_password1='pswd1'

test_email2='test2@sample.com'
test_password2='pswd2'


class UserModelTest(TestCase):
    def test_create_user(self):
        ''' Userインスタンスが正しく生成できるかをテスト '''

        self.assertEqual(User.objects.all().count(), 0)

        user = User.objects.create(email=test_email1, password=test_password1)

        self.assertEqual(User.objects.all().count(), 1)

        self.assertEqual(user.email, test_email1)
        self.assertEqual(user.password, test_password1)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, True)


    def test_update_user(self):
        ''' Userインスタンスを正しく変更できるかをテスト '''

        user = User.objects.create(email='test1@sample.com', password='pswd1')

        self.assertEqual(User.objects.all().count(), 1)

        user.email = test_email2
        user.password = test_password2
        user.is_superuser = True
        user.is_staff = True
        user.is_active = False
        user.save()

        self.assertEqual(User.objects.all().count(), 1)

        self.assertEqual(user.email, test_email2)
        self.assertEqual(user.password, test_password2)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, False)