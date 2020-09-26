"""Defines url patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'main_app'

urlpatterns = [
    # Home page.
    path('', views.IndexView.as_view(), name='index'),

    # Show all topics.
    path('topics/', views.topics, name='topics'),

    # Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # Page for adding a new topic
    path('new_topic/', views.new_topic, name='new_topic'),

    # Page for adding a new entry
    path('opics/<int:topic_id>/new_entry', views.new_entry, name='new_entry'),

    # Page for editting an existence entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry')
]
