from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.forms import (
    TaskForm,
    TaskSearchForm,
    WorkerCreationForm,
    WorkerSearchForm,
    ProjectCreationForm,
    ProjectSearchForm,
    TeamCreationForm,
    TeamSearchForm,
    PositionSearchForm,
    TaskTypeSearchForm,
)
from manager.models import Team, Project, TaskType, Task, Position


class BaseFormTest(TestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = get_user_model().objects.create_superuser(
            username="TestAdmin",
            password="testpass12345",
        )
        self.client.force_login(self.admin_user)

        self.team = Team.objects.create(
            name="TestTeam",
        )
        self.team.members.set([self.admin_user])

        self.project = Project.objects.create(
            name="TestProject",
            status="working",
        )
        self.project.team.set([self.team])

        self.task_type = TaskType.objects.create(name="TestTaskType")

        self.task = Task.objects.create(
            name="test_task",
            deadline="2031-01-01",
            is_completed=False,
            priority="medium",
            task_type=self.task_type,
            project=self.project,
        )
        self.task.assignees.set([self.admin_user])

        self.position = Position.objects.create(
            name="test_position",
        )


class TaskFormTest(BaseFormTest):
    def test_task_creation_form_with_completed_status_non_valid(self):
        form_data = {
            "name": "TestTask",
            "deadline": "2023-03-03",
            "is_completed": True,
            "priority": "low",
            "task_type": self.task_type.id,
            "assignees": [self.admin_user.id],
            "project": self.project.id,
        }

        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_search(self):
        form_data = {"keyword": "test"}
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class WorkerFormTest(BaseFormTest):
    def test_worker_form_with_position_first_last_name_is_valid(self):
        form_data = {
            "username": "username",
            "password1": "passtes45",
            "password2": "passtes45",
            "first_name": "test first",
            "last_name": "test last",
            "position": self.position,
        }
        form = WorkerCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_search_username_first_last_name(self):
        form_data = {"keyword": "test"}
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ProjectFormTest(BaseFormTest):
    def test_project_creation_with_completed_status_non_valid(self):
        form_data = {
            "name": "TestProject",
            "status": "completed",
            "team": [self.team.id],
        }

        form = ProjectCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_project_search(self):
        form_data = {"name": "test"}
        form = ProjectSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TeamFormTest(BaseFormTest):
    def test_team_creation_is_valid(self):
        form_data = {"name": "TestTeam", "members": [self.admin_user]}
        form = TeamCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "TestTeam")
        self.assertEqual(list(form.cleaned_data["members"]), [self.admin_user])

    def test_team_search_name(self):
        form_data = {"name": "test"}
        form = TeamSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class PositionFormTest(BaseFormTest):
    def test_position_search_name(self):
        form_data = {"name": "test"}
        form = PositionSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskTypeFormTest(BaseFormTest):
    def test_task_type_search_name(self):
        form_data = {"name": "test"}
        form = TaskTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
