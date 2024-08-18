from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import Tasks


# Create your views here.
def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
  
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["username"]
                )
                user.save()
                login(request, user)
            except:
                return render(
                    request,
                    "signup.html",
                    context={
                        "form": UserCreationForm,
                        "error": "Username already exists",
                    },
                )
            return redirect("tasks")
        else:
            return render(
                request,
                "signup.html",
                context={"form": UserCreationForm,
                         "error": "Password do not match"},
            )

    return render(request, "signup.html", context={"form": UserCreationForm})


def homepage(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", context={"form": UserCreationForm})

@login_required
def signout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")


def signin(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        user = authenticate(
            request=request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("home")

    return render(request, "signin.html", {"form": AuthenticationForm})


@login_required
def tasks(request: HttpRequest) -> HttpResponse:
    tasks = Tasks.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, "tasks.html", {"tasks": tasks})

@login_required
def task_completed(request: HttpRequest) -> HttpResponse:
    tasks = Tasks.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')

    return render(request, "tasks.html", {"tasks": tasks})

@login_required
def task_detail(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST, instance=task)
            form.save(commit=True)
            return redirect('tasks')
        except:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating'})
    form = TaskForm(instance=task)
    return render(request, 'task_detail.html', {'task': task, 'form': form})


@login_required
def complete_task(request, task_id) -> HttpResponse:
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id) -> HttpResponse:
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def create_task(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except:
            return render(
                request,
                "create_tasks.html",
                {"form": TaskForm, "error": "Please, provide valid values"},
            )

    return render(request, "create_tasks.html", {"form": TaskForm})
