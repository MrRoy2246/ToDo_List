from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user,is_deleted=False)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['deleted_task_count'] = Task.objects.filter(user=self.request.user, is_deleted=True).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


# class DeleteView(LoginRequiredMixin, DeleteView):
#     model = Task
#     context_object_name = 'task'
#     success_url = reverse_lazy('tasks')
#     def get_queryset(self):
#         owner = self.request.user
#         return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
    




# ================================practice

class SoftDeleteTask(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, id=pk, user=request.user)
        task.is_deleted = True
        task.save()
        return redirect('tasks')


class RecycleBinView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'deleted_tasks'
    template_name = 'base/bin.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, is_deleted=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the count of deleted tasks to the context
        context['deleted_task_count'] = context['deleted_tasks'].count()
        return context


class RestoreTask(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, id=pk, user=request.user)
        task.is_deleted = False
        task.save()
        return redirect('recycle-bin')


class PermanentlyDeleteTask(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, id=pk, user=request.user)
        task.delete()
        return redirect('recycle-bin')
