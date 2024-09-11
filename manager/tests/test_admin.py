from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Position


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_admin = get_user_model().objects.create_superuser(
            username="admin", password="admin753"
        )
        self.client.force_login(self.user_admin)
        self.position = Position.objects.create(name="test_position")
        self.worker = get_user_model().objects.create_user(
            username="test", password="test15975", position=self.position
        )

    def test_worker_position_listed(self):
        url = reverse("admin:manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_detail_position_listed(self):
        url = reverse("admin:manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)
