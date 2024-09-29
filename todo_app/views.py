from django.shortcuts import render, redirect, get_object_or_404
from .models import Todos
from .forms import ListForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url="/login/")
def index(request):
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo başarıyla oluşturuldu.')
            return redirect('index')
    else:
        form = ListForm()

    todo_list = Todos.objects.filter(user=request.user).order_by('-priority', 'due_date')

    search_bar = request.GET.get("q")
    if search_bar:
        todo_list = todo_list.filter(title__icontains=search_bar)

    today = timezone.now().date()

    overdue_tasks = todo_list.filter(due_date__lt=today, finished=False)
    if overdue_tasks.exists():
        messages.warning(request, f'{overdue_tasks.count()} adet görev son tarihi geçmiş durumda!')

    upcoming_tasks = todo_list.filter(due_date=today, finished=False)
    if upcoming_tasks.exists():
        messages.info(request, f'{upcoming_tasks.count()} adet görev bugün için planlanmış!')

    context = {
        "todo_list": todo_list,
        "search_bar": search_bar,
        "form": form,
        "today": today,
    }
    return render(request, "todo_app/index.html", context)

@login_required(login_url="/login/")
def about(request):
    return render(request, "todo_app/about.html")

@login_required(login_url="/login/")
def create(request):
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo başarıyla oluşturuldu.')
            return redirect('index')
    else:
        form = ListForm()
    
    return render(request, "todo_app/create.html", {'form': form})

@login_required(login_url="/login/")
def delete(request, Todos_id):
    todo = get_object_or_404(Todos, pk=Todos_id)
    todo.delete()
    messages.success(request, 'Todo başarıyla silindi.')
    return redirect("index")

@login_required(login_url="/login/")
def yes_finish(request, Todos_id):
    todo = get_object_or_404(Todos, pk=Todos_id)
    todo.finished = False
    todo.save()
    messages.success(request, 'Todo tamamlanmamış olarak işaretlendi.')
    return redirect("index")

@login_required(login_url="/login/")
def no_finish(request, Todos_id):
    todo = get_object_or_404(Todos, pk=Todos_id)
    todo.finished = True
    todo.save()
    messages.success(request, 'Todo tamamlanmış olarak işaretlendi.')
    return redirect("index")

@login_required(login_url="/login/")
def update(request, Todos_id):
    todo_item = get_object_or_404(Todos, pk=Todos_id)
    
    if request.method == "POST":
        form = ListForm(request.POST, instance=todo_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo başarıyla güncellendi.')
            return redirect("index")
        else:
            messages.error(request, "Formda hatalar var. Lütfen kontrol edin.")
    else:
        form = ListForm(instance=todo_item)
    
    return render(request, "todo_app/update.html", {'form': form, 'todo': todo_item})

@login_required(login_url="/login/")
def search(request):
    query = request.GET.get('query')
    results = []
    
    if query:
        results = Todos.objects.filter(title__icontains=query)

    return render(request, 'index.html', {'results': results, 'query': query})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesabınız oluşturuldu! Şimdi giriş yapabilirsiniz.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
