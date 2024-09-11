from django.urls import path

from manager.views import (
    IndexView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("worker/create", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "worker/<int:pk>/update",
        WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "worker/<int:pk>/delete",
        WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "position/create", PositionCreateView.as_view(), name="position-create"
    ),
    path(
        "position/<int:pk>/update",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "position/<int:pk>/delete",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task-type/create",
        TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path(
        "task-type/<int:pk>/update",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "task-type/<int:pk>/delete",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "project/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"
    ),
    path(
        "project/create/", ProjectCreateView.as_view(), name="project-create"
    ),
    path(
        "project/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "project/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("team/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
    path(
        "team/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"
    ),
    path(
        "team/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"
    ),
]

app_name = "manager"
