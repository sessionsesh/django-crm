from django.test import TestCase
from accounts.models import User

# Create your tests here.


class UserTestCase(TestCase):

    def test_roles_creation(self):
        User.objects.create_customer(
            username='customer', email='customer@cmr.com', password='customer')

        User.objects.create_employee(
            username='employee', email='employee@cmr.com', password='employee')

        User.objects.create_admin(
            username='admin', email='admin@cmr.com', password='admin')

        self.assertEqual(User.objects.count(), 3)

    def test_user_create_delete(self):
        # Check for correct creation
        for i in range(10):
            User.objects.create_user(
                username=f'user{i}', password=f'password{i}', email=f'user{i}@crm.com')
        users = User.objects.all()
        for i in range(10):
            self.assertEqual(users[i].username, f'user{i}')

        # Check for correct deletion
        for user in users:
            user.delete()
        total_users_count = User.objects.count()
        self.assertEqual(total_users_count, 0)

        # self.assertEqual('x', 'y')

    def test_user_read_update(self):
        username_to_update = 'update_me_user'
        updated_username = 'updated_user'

        # Create user
        User.objects.create_user(
            username=username_to_update, password='password', email='user@crm.com')

        # Read check
        self.assertEqual(User.objects.get(
            username=username_to_update).email, 'user@crm.com')

        # Update check
        if User.objects.filter(username=updated_username).exists():
            raise ValueError('This useranme already exists.')
        user = User.objects.get(
            username=username_to_update)
        user.username = updated_username
        user.save()

        self.assertEqual(User.objects.get(
            email='user@crm.com').username, updated_username)
