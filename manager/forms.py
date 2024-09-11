from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q, QuerySet
from django.utils import timezone

from manager.models import Worker, Task, Position, Project, Team, TaskType


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        is_update = kwargs.pop("is_update", False)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-4 mb-0"),
                Column("deadline", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("project", css_class="form-group col-md-4 mb-0"),
                Column("priority", css_class="form-group col-md-2 mb-0"),
                Column("task_type", css_class="form-group col-md-2 mb-0"),
            ),
            Row(
                Column(
                    "is_completed",
                    css_class="d-none"
                    if not is_update
                    else "form-group col-md-2",
                ),
            ),
            Row(
                Column("description", css_class="form-group col-md-8 mb-0"),
            ),
            Row(
                Column(
                    "assignees",
                    css_class="form-group col-md-4 h-50 mb-4",
                    style="max-height: 600px; overflow-y: auto;",
                ),
            ),
            Row(
                Column(Submit("submit", "Save", css_class="btn btn-primary")),
            ),
        )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        now = timezone.now()

        if deadline < now:
            raise ValidationError(
                "Deadline can't be earlier than current date"
            )

        return deadline


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all())

    class Meta(UserCreationForm):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("username", css_class="form-group col-md-4 mb-0"),
                Column("position", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("first_name", css_class="form-group col-md-4 mb-0"),
                Column("last_name", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("password1", css_class="form-group col-md-4 mb-0"),
                Column("password2", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column(Submit("submit", "Save", css_class="btn btn-primary")),
            ),
        )


class WorkerUpdateForm(forms.ModelForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all())

    class Meta(UserCreationForm):
        model = Worker
        fields = ["position", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="form-group col-md-4 mb-0"),
                Column("last_name", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("position", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column(Submit("submit", "Save", css_class="btn btn-primary")),
            ),
        )


class ProjectCreationForm(forms.ModelForm):
    team = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        is_update = kwargs.pop("is_update", False)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "name",
                    css_class="form-group col-md-4"
                    if is_update
                    else "form-group col-md-8",
                ),
                Column(
                    "status",
                    css_class="d-none"
                    if not is_update
                    else "form-group col-md-4",
                ),
            ),
            Row(
                Column("description", css_class="form-group col-md-8 mb-0"),
            ),
            Row(
                Column(
                    "team",
                    css_class="form-group col-md-8 mb-0",
                    style="max-height: 600px; overflow-y: auto;",
                ),
            ),
            Row(
                Column(Submit("submit", "Save", css_class="btn btn-primary")),
            ),
        )

    def clean_status(self):
        status = self.cleaned_data.get("status")

        if self.instance.pk is None and status == "completed":
            raise ValidationError(
                "Status can't be set as 'completed' during project creation."
            )

        return status


class TeamCreationForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column(
                    "members",
                    css_class="form-group col-md-4 h-50 mb-4",
                    style="max-height: 600px; overflow-y: auto;",
                ),
            ),
            Row(
                Column(Submit("submit", "Save", css_class="btn btn-primary")),
            ),
        )


class PositionCreationForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column(
                    Submit(
                        "submit", "Add position", css_class="btn btn-primary"
                    )
                ),
            ),
        )


class TaskTypeCreationForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column(
                    Submit(
                        "submit", "Add task type", css_class="btn btn-primary"
                    )
                ),
            ),
        )


class WorkerSearchForm(forms.Form):
    keyword = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Are you looking for somebody?"}
        ),
    )

    def search(self) -> QuerySet:
        keyword = self.cleaned_data.get("keyword")

        workers = Worker.objects.all()

        if keyword:
            workers = workers.filter(
                Q(username__icontains=keyword)
                | Q(first_name__icontains=keyword)
                | Q(last_name__icontains=keyword)
            )

        return workers


class TaskSearchForm(forms.Form):
    keyword = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Looking for task?"}),
    )

    def search(self) -> QuerySet:
        keyword = self.cleaned_data.get("name")

        tasks = Task.objects.all()

        if keyword:
            tasks = tasks.filter(name__icontains=keyword)

        return tasks


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Looking for position?"}),
    )


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Looking for task type?"}
        ),
    )


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Looking for project?"}),
    )


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Looking for team?"}),
    )
