from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserActivityLog

class UserActivityLogTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='pass123')
        self.client.login(username='john', password='pass123')

    def test_create_log(self):
        response = self.client.post('/activity-logs/', {
            "action": "LOGIN",
            "metadata": {"ip": "127.0.0.1"}
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_logs(self):
        UserActivityLog.objects.create(user=self.user, action="LOGIN")
        response = self.client.get('/activity-logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transition_status(self):
        log = UserActivityLog.objects.create(user=self.user, action="LOGIN")
        url = f'/activity-logs/{log.id}/transition/'
        response = self.client.patch(url, {"status": "DONE"})
        self.assertEqual(response.status_code, 200)
        log.refresh_from_db()
        self.assertEqual(log.status, "DONE")

    def test_caching_behavior(self):
        from django.core.cache import cache
        cache.clear()
        UserActivityLog.objects.create(user=self.user, action="LOGIN")
        self.client.get('/activity-logs/?action=LOGIN')
        self.assertIsNotNone(cache.get(f"user_activity_{self.user.id}_/activity-logs/?action=LOGIN"))