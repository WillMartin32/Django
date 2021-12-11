from django.shortcuts import render, redirect
from .forms import EntryForm, TopicForm
from .models import Topic, Entry
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    return render(request, 'MainApp/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')

    # The key is the variable used in the html file and value is variable usd in the view function
    context = {'topics':topics}

    return render(request, 'MainApp/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.all()

    context = {'topic':topic, 'entries':entries}

    return render(request, 'MainApp/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)

        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()


            return redirect('MainApp:topics')

    context = {'form':form} # context is a dictionary that allows use to pass data to our template. Pass form to html file
    return render(request, 'MainApp/new_topic.html', context)

@login_required
def new_entry(request, topic_id): # Have to use same name as in url file (topic_id). If you change one have to change the other.
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()

            return redirect('MainApp:topic', topic_id=topic_id)

    context = {'form':form, 'topic':topic}
    return render(request, 'MainApp/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    #if topic != request.user:
    #    raise Http404

    if request.method != 'POST':
        # This argument tells Django to create the form prefilled
        # with information from the existing entry object.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('MainApp:topic', topic_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form': form}
    return render(request, 'MainApp/edit_entry.html', context)