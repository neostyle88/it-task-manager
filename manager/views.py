from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import (
    TaskForm,
    WorkerCreationForm,
    TaskSearchForm,
    WorkerSearchForm,
    PositionSearchForm,
    TaskTypeSearchForm,
    ProjectCreationForm,
    TeamCreationForm,
    ProjectSearchForm,
    TeamSearchForm,
    PositionCreationForm,
    TaskTypeCreationForm,
    WorkerUpdateForm,
)
from manager.models import Worker, Task, TaskType, Position, Project, Team


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "manager/index.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        user = self.request.user

        user_tasks_stats = (
            Task.objects.prefetch_related("assignees")
            .filter(assignees=user)
            .aggregate(
                total_tasks=Count("id"),
                completed_tasks=Count("id", filter=Q(is_completed=True)),
            )
        )
        context["user_tasks_count"] = user_tasks_stats["total_tasks"]
        context["user_done_tasks_count"] = user_tasks_stats["completed_tasks"]

        user_projects_stats = (
            Project.objects.prefetch_related("team")
            .filter(tasks__assignees=user)
            .aggregate(
                total_projects=Count("id", distinct=True),
                completed_projects=Count("id", filter=Q(status="completed")),
            )
        )
        context["user_projects_count"] = user_projects_stats["total_projects"]
        context["user_done_projects_count"] = user_projects_stats["completed_projects"]

        project_list = Project.objects.all()
        for project in project_list:
            completed_tasks = project.tasks.filter(is_completed=True).count()
            total_tasks = project.tasks.count()

            if total_tasks > 0:
                project.percent = round((completed_tasks / total_tasks) * 100)
            else:
                project.percent = 0

        context["project_list"] = project_list

        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "manager/task_list.html"
    paginate_by = 4
    queryset = Task.objects.select_related("task_type").all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            if keyword is not None:
                queryset = Task.objects.filter(name__icontains=keyword)
            else:
                queryset = Task.objects.all()
            return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["is_update"] = True
        return kwargs


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    paginate_by = 10
    queryset = Worker.objects.all().select_related("position")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = WorkerSearchForm(data=self.request.GET or None)
        context["search_form"] = search_form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = WorkerSearchForm(data=self.request.GET)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            if keyword:
                queryset = queryset.filter(
                    Q(username__icontains=keyword)
                    | Q(first_name__icontains=keyword)
                    | Q(last_name__icontains=keyword)
                )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "manager/position_list.html"
    paginate_by = 10
    queryset = Position.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        position = self.request.GET.get("position")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        context["num_of_people_in_position"] = Worker.objects.filter(
            position=position
        ).count()

        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])

        return self.queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionCreationForm
    success_url = reverse_lazy("manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "manager/task_type_list.html"
    paginate_by = 10
    queryset = TaskType.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = TaskTypeSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])

        return self.queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeCreationForm
    success_url = reverse_lazy("manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager:task-type-list")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        pk = kwargs["object"].id
        project = Project.objects.get(pk=pk)
        context["completed_tasks"] = project.tasks.filter(is_completed=True)
        context["uncompleted_tasks"] = project.tasks.filter(is_completed=False)

        return context


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5
    queryset = Project.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ProjectSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = ProjectSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name is not None:
                queryset = Project.objects.filter(name__icontains=name)
            else:
                queryset = Project.objects.all()
            return queryset


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreationForm
    success_url = reverse_lazy("manager:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectCreationForm
    success_url = reverse_lazy("manager:project-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["is_update"] = True
        return kwargs


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("manager:project-list")


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TeamSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = TeamSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name is not None:
                queryset = Team.objects.filter(name__icontains=name)
            else:
                queryset = Team.objects.all()
            return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    queryset = Team.objects.all()


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreationForm
    success_url = reverse_lazy("manager:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamCreationForm
    success_url = reverse_lazy("manager:team-list")


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("manager:team-list")
