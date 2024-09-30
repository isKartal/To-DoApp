from django.shortcuts import render, redirect, get_object_or_404
from .models import Todos
from .forms import ListForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone

def index(request):
    if request.user.is_authenticated:
        # Giriş yapan kullanıcıların görevlerini göster
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

        today = timezone.now().date()

        search_bar = request.GET.get("q")
        if search_bar:
            todo_list = todo_list.filter(title__icontains=search_bar)

        overdue_tasks = todo_list.filter(due_date__lt=today, finished=False)
        if overdue_tasks.exists():
            messages.warning(request, f'{overdue_tasks.count()} adet görev son tarihi geçmiş durumda!')

        upcoming_tasks = todo_list.filter(due_date__date=today, finished=False)
        if upcoming_tasks.exists():
            messages.info(request, f'{upcoming_tasks.count()} adet görev bugün için planlanmış!')

        context = {
            "todo_list": todo_list,
            "search_bar": search_bar,
            "form": form,
            "today": today,
        }
    else:
        # Giriş yapmayan kullanıcılar için sadece public görevleri göstereceğiz.
        todo_list = Todos.objects.filter(public=True).order_by('-priority', 'due_date')  
        messages.info(request, "Daha fazla işlem yapmak için giriş yapmalısınız.")

        today = timezone.now().date()

        context = {
            "todo_list": todo_list,
            "search_bar": None,
            "today": today,
        }

    return render(request, "todo_app/index.html", context)


def about(request):
    if not request.user.is_authenticated:
        messages.info(request, "Bu sayfayı görüntülemek için giriş yapmalısınız.")
        return redirect('index')
    
    return render(request, "todo_app/about.html")

def create(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ListForm(request.POST)
            if form.is_valid():
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                messages.success(request, 'Todo başarıyla oluşturuldu.')
                return redirect('index')
        else:
            messages.info(request, "Bu işlemi gerçekleştirmek için lütfen önce giriş yapın!")

    form = ListForm()  # Formu her zaman göster
    return render(request, "todo_app/create.html", {'form': form})

def delete(request, Todos_id):
    if request.user.is_authenticated:
        todo = get_object_or_404(Todos, pk=Todos_id)
        todo.delete()
        messages.success(request, 'Todo başarıyla silindi.')
    else:
        messages.info(request, "Bu işlemi gerçekleştirmek için lütfen önce giriş yapın!")
    
    return redirect("index")

def yes_finish(request, Todos_id):
    if request.user.is_authenticated:
        todo = get_object_or_404(Todos, pk=Todos_id)
        todo.finished = False
        todo.save()
        messages.success(request, 'Todo tamamlanmamış olarak işaretlendi.')
    else:
        messages.info(request, "Bu işlemi gerçekleştirmek için lütfen önce giriş yapın!")
    
    return redirect("index")

def no_finish(request, Todos_id):
    if request.user.is_authenticated:
        todo = get_object_or_404(Todos, pk=Todos_id)
        todo.finished = True
        todo.save()
        messages.success(request, 'Todo tamamlanmış olarak işaretlendi.')
    else:
        messages.info(request, "Bu işlemi gerçekleştirmek için lütfen önce giriş yapın!")
    
    return redirect("index")

def update(request, Todos_id):
    if request.user.is_authenticated:
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
    
    messages.info(request, "Bu işlemi gerçekleştirmek için lütfen önce giriş yapın!")
    return redirect("index")

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
