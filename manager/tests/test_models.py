from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import Position, TaskType, Team, Project, Task


class ModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position")
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

    def test_position_str(self):
        self.assertEqual(
            str(self.position),
            self.position.name,
        )

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.username} "
            f"({self.worker.first_name} {self.worker.last_name})",
        )

    def test_task_type_str(self):
        self.assertEqual(
            str(self.task_type),
            self.task_type.name,
        )

    def test_team_str(self):
        self.assertEqual(
            str(self.team),
            self.team.name,
        )

    def test_project_str(self):
        self.assertEqual(
            str(self.project),
            self.project.name,
        )

    def test_task_str(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.name} ({self.task.priority})",
        )

    def test_task_update_project_status(self):
        self.assertEqual(
            self.project.status,
            "working",
        )
        self.task.is_completed = True
        self.task.save()
        self.assertEqual(
            self.project.status,
            "completed",
        )
