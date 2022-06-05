from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout #login as auth_login to avoide error on login view as same name of view
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ToDo

def todo(request):
    tasks = None
    if request.user.is_authenticated:
        tasks = ToDo.objects.filter(user=request.user)

    if request.user.is_authenticated:
        if request.method == 'POST':
            task = request.POST.get('task')
            user = request.user

            todo_obj = ToDo.objects.create(user=user, task=task)
            todo_obj.save()
            return redirect('/')
    else:
        messages.warning(request, "Please login first")
        return redirect('/login/')
    
    edit_task = None
    slug = ""
    if request.method == 'GET':
        slug = request.GET.get('edit')
    if slug != "" or slug != None:
        edit_task = ToDo.objects.filter(slug=slug).first()
    
    context = {'tasks': tasks.reverse(), 'edit_task': edit_task}
    return render(request, 'todo.html', context)

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        try:
            if User.objects.filter(username=username).exists() and username != "":
                messages.success(request, f"{username} - this username already exists, try another")
                return redirect('/registration/')
            if len(email) > 7:
                if User.objects.filter(email=email).exists():
                    messages.success(request, f"{email} - this email already exists, try another")
                    return redirect('/registration/')
            if len(email) < 7:
                email = "...@gmail.com"
            if len(password) < 4 or password == "" or password == " ":
                messages.success(request, "Please, Enter atleast 4 charecter as your password.")
                return redirect("/registration/")
            if password != password2:
                messages.success(request, "Please, Enter the same password.")
                return redirect("/registration/")
            try:
                user_obj = User.objects.create_user(username=username, email=email)
                user_obj.set_password(password)
                user_obj.save()
                messages.success(request, "Successfuly account created. You can login now")
                return redirect("/login/")
            except Exception as e:
                messages.success(request, "Something went wrong on registration")
                return redirect("/registration/")
        except Exception as e:
            messages.success(request, "Something went wrong!")
            return redirect(request, "/registration/")
    return render(request, 'registration.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).first() is None:
            messages.success(request, f"{username} - this username doesn't exists!")
            return redirect("/login/")
        else:
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.success(request, "Wrong username or password")
                return redirect("/login/")
            else:
                auth_login(request, user)
                messages.success(request, f"{username} - Login successful")
                return redirect("/")

    return render(request, 'login.html')

def logout(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'You wasn\'t Logged-In.')
        return redirect('/login/')
    
    auth_logout(request)
    messages.success(request, "You are Logged-Out!")
    return redirect('/login/')

def task_complete(request, slug):
    task = ToDo.objects.get(slug=slug)
    if task.is_complete == False:
        task.is_complete = True
        task.save()
        messages.success(request, "Task Completed")
    else:
        task.is_complete = False
        task.save()
    return redirect('/')
def edit(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        inp_task = request.POST.get('edit_text')
        print(inp_task, slug)

        task_obj = ToDo.objects.filter(slug=slug).first()
        task_obj.task = inp_task
        task_obj.save()

        messages.success(request, "Updated successful")
    return redirect('/')
def delete(request, slug):
    delete_task = ToDo.objects.filter(slug=slug).first()
    delete_task.delete()
    messages.success(request, "Successfuly deleted")
    return redirect('/')

def profile(request):
    return render(request, 'profile.html')