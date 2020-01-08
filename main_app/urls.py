from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<uuid:id>', views.DetailView.as_view(), name='detail'),
    path('new', views.NewView.as_view(), name='new'),
    path('create', views.CreateView.as_view(), name='create'),
    path('<uuid:id>/edit', views.EditView.as_view(), name='edit'),
    path('<uuid:id>/update', views.UpdateView.as_view(), name='update'),
    path('<uuid:id>/delete', views.DeleteView.as_view(), name='delete'),
    path('<uuid:id>/vote', views.VoteView.as_view(), name='vote'),
]