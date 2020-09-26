from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

class IndexView(generic.TemplateView):
    """The home page for Learning Log."""
    template_name = 'main_app/index.html'

@login_required
def topics(request):
    """Show all topics."""
    topics_list = get_list_or_404(Topic.objects.order_by('date_added'), owner=request.user)

    context = {'topics': topics_list}

    return render(request, 'main_app/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic, and all its entries."""
    topic_obj = get_object_or_404(Topic, id=topic_id)

    if topic_obj.owner != request.user:
        raise Http404

    entries = topic_obj.entry_set.order_by('-date_added')
    context = {'topic': topic_obj, 'entries': entries}

    return render(request, 'main_app/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_one = form.save(commit=False)
            new_one.owner = request.user
            new_one.save()
            return HttpResponseRedirect(reverse('main_app:topics'))

    context = {'form': form}

    return render(request, 'main_app/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic_obj = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_one = form.save(commit=False)
            new_one.topic = topic
            new_one.save()
            return HttpResponseRedirect(reverse('main_app:topic', args=[topic_id]))

    context = {'topic': topic_obj, 'form': form}

    return render(request, 'main_app/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry_obj = get_object_or_404(Entry, id=entry_id)
    topic_obj = entry_obj.topic

    if topic_obj.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry_obj)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry_obj, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main_app:topic', args=[topic_obj.id]))

    context = {'entry': entry_obj, 'topic': topic_obj, 'form': form}

    return render(request, 'main_app/edit_entry.html', context)
