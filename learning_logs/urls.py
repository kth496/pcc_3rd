from django.urls import path  # (2)

from . import views  # (3)

app_name = 'learning_logs'  # (4)
urlpatterns = [  # (5)
    # 홈페이지
    path('', views.index, name='index'),  # (6)
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
