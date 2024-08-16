from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from tasks.forms import TaskForm


# Create your views here.
def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        print(request.POST)
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
                context={"form": UserCreationForm, "error": "Password do not match"},
            )

    return render(request, "signup.html", context={"form": UserCreationForm})


def homepage(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", context={"form": UserCreationForm})


def tasks(request) -> HttpResponse:
    return render(request, "tasks.html")


def signout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")


def signin(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        user = authenticate(
            request,
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
            return redirect('home')

    return render(request, "signin.html", {"form": AuthenticationForm})


def create_task(request:HttpRequest) -> HttpResponse:
    return render(request, 'create_tasks.html', {
        'form': TaskForm
    })