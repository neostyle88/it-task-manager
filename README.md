# Task Manager

Task Manager is a web application built with Django that allows you to manage projects,
teams, employees, tasks, positions, and task types.
It provides a user-friendly interface for organizing and tracking tasks within an organization or team.

---

## Features

>- Create, update, and delete projects
>- Assign teams to projects
>- Manage employees and their roles within the organization
>- Categorize tasks based on task types
>- Track the status of tasks (working, completed, canceled)
>- Generate reports and view project progress

---

## Local deployment instruction

>To deploy the Task Manager project locally, please follow the steps below:

1. Clone the repository to your local machine:
   ```git clone https://github.com/neostyle88/it-task-manager.git```

2. Navigate to the project directory:
   ```cd it_task_manager```

3. Create a virtual environment:
   ```python -m venv env```

4. Activate the virtual environment:
   - For Windows:
   ``` .\env\Scripts\activate```
   - For macOS and Linux:
   ```source env/bin/activate```

5. Install the project dependencies:
   ```pip install -r requirements.txt```

6. Apply database migrations:
   ```python manage.py migrate```

7. Run the development server:
   ```python manage.py runserver```

8. Open your web browser and access the Task Manager application at http://localhost:8000/.

> You can use test user made during migration:

   - Username ```admin```
   - Password ```testpass123```

---
## Environment Variables

>The following environment variables should be set in the `.env` file:

- `DJANGO_SECRET_KEY`: Your Django secret key

**Note:** Before starting the project, make a copy of the `.env_sample` file and rename it to `.env`. Replace the sample values with your actual environment variable values.