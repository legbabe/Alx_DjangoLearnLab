from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.client.login(username='user1', password='pass')

    def test_follow_user(self):
        url = reverse('follow-user', args=[self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_user(self):
        self.user1.following.add(self.user2)
        url = reverse('unfollow-user', args=[self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class FeedTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.client.login(username='user1', password='pass')
        # Assume there are posts created by user2 here

    def test_user_feed(self):
        self.user1.following.add(self.user2)
        url = reverse('user-feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

