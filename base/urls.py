from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, CustomLoginView, RegisterPage, TaskReorder,SoftDeleteTask,RecycleBinView,RestoreTask,PermanentlyDeleteTask,DeleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    # path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
    path('task/<int:pk>/soft-delete/', SoftDeleteTask.as_view(), name='task-soft-delete'),
    path('recycle-bin/', RecycleBinView.as_view(), name='recycle-bin'),
    path('task/<int:pk>/restore/', RestoreTask.as_view(), name='task-restore'),
    path('task/<int:pk>/permanent-delete/', PermanentlyDeleteTask.as_view(), name='task-permanent-delete'),





]