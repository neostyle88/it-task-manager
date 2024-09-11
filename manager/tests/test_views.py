from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Position, Team, TaskType, Project, Task, Worker

POSITION_LIST_URL = reverse("manager:position-list")
WORKER_LIST_URL = reverse("manager:worker-list")
WORKER_DETAIL_URL = reverse("manager:worker-detail", kwargs={"pk": 1})
TASK_TYPE_LIST_URL = reverse("manager:task-type-list")
TEAM_LIST_URL = reverse("manager:team-list")
PROJECT_LIST_URL = reverse("manager:project-list")
PROJECT_DETAIL_URL = reverse("manager:project-detail", kwargs={"pk": 1})
TASK_LIST_URL = reverse("manager:task-list")
TASK_DETAIL_URL = reverse("manager:task-detail", kwargs={"pk": 1})


class BasePrivateTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.position = Position.objects.create(name="test_position")
        self.admin_user = get_user_model().objects.create_superuser(
            username="user.admin", password="testpassword12589"
        )
        self.client.force_login(self.admin_user)

        self.worker = get_user_model().objects.create_user(
            username="TestWorker",
            password="testpass12345",
            first_name="Test first",
            last_name="Test last",
        )

        self.task_type = TaskType.objects.create(name="test_task")
        self.team = Team.objects.create(name="test_team")
        self.team.members.set([self.worker])
        self.project = Project.objects.create(
            name="test_project",
            status="working",
        )
        self.project.team.set([self.team])
        self.task = Task.objects.create(
            name="test_task",
            deadline="2031-01-01",
            is_completed=False,
            priority="medium",
            task_type=self.task_type,
            project=self.project,
        )
        self.task.assignees.set([self.worker])


class PrivatePositionTest(BasePrivateTest):
    def test_retrieve_position_list(self):
        response = self.client.get(POSITION_LIST_URL)
        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]), list(positions)
        )
        self.assertTemplateUsed(response, "manager/position_list.html")


class PrivateWorkerTest(BasePrivateTest):
    def test_retrieve_worker_list(self):
        response = self.client.get(WORKER_LIST_URL)
        workers = Worker.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["worker_list"]), list(workers))
        self.assertTemplateUsed(response, "manager/worker_list.html")

    def test_retrieve_worker_detail(self):
        response = self.client.get(WORKER_DETAIL_URL)
        worker = get_user_model().objects.get(id=self.admin_user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["worker"], worker)
        self.assertTemplateUsed(response, "manager/worker_detail.html")


class PrivateTaskTypeTest(BasePrivateTest):
    def test_retrieve_task_type_list(self):
        response = self.client.get(TASK_TYPE_LIST_URL)
        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]), list(task_types)
        )
        self.assertTemplateUsed(response, "manager/task_type_list.html")


class PrivateTeamTest(BasePrivateTest):
    def test_retrieve_team_list(self):
        response = self.client.get(TEAM_LIST_URL)
        teams = Team.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["team_list"]), list(teams))
        self.assertTemplateUsed(response, "manager/team_list.html")


class PrivateProjectTest(BasePrivateTest):
    def test_retrieve_project_list(self):
        response = self.client.get(PROJECT_LIST_URL)
        projects = Project.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["project_list"]), list(projects)
        )
        self.assertTemplateUsed(response, "manager/project_list.html")

    def test_retrieve_project_detail(self):
        response = self.client.get(PROJECT_DETAIL_URL)
        project = Project.objects.get(id=self.project.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["project"], project)
        self.assertTemplateUsed(response, "manager/project_detail.html")


class PrivateTaskTest(BasePrivateTest):
    def test_retrieve_task_list(self):
        response = self.client.get(TASK_LIST_URL)
        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["task_list"]), list(tasks))
        self.assertTemplateUsed(response, "manager/task_list.html")

    def test_retrieve_task_detail(self):
        response = self.client.get(TASK_DETAIL_URL)
        task = Task.objects.get(id=self.task.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["task"], task)
        self.assertTemplateUsed(response, "manager/task_detail.html")


class PublicPositionTest(TestCase):
    def test_list_login_reqired(self):
        res = self.client.get(POSITION_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_detail_login_reqired(self):
        res = self.client.get(POSITION_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicWorkerTest(TestCase):
    def test_list_login_reqired(self):
        res = self.client.get(WORKER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_detail_login_reqired(self):
        res = self.client.get(WORKER_DETAIL_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicTaskTypeTest(TestCase):
    def test_list_login_reqired(self):
        res = self.client.get(TASK_TYPE_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicTeamTest(TestCase):
    def test_list_login_reqired(self):
        res = self.client.get(POSITION_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicProjectTest(TestCase):
    def test_list_login_reqired(self):
        res = self.client.get(PROJECT_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_detail_login_reqired(self):
        res = self.client.get(PROJECT_DETAIL_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicTaskTest(TestCase):
    def test_task_list_login_reqired(self):
        res = self.client.get(TASK_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_detail_login_reqired(self):
        res = self.client.get(TASK_DETAIL_URL)

        self.assertNotEqual(res.status_code, 200)
