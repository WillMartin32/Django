from django.shortcuts import render, redirect

from .forms import EntryForm, TopicForm

from .models import Topic

# Create your views here.
def index(request):
    return render(request, 'MainApp/index.html')


def topics(request):
    topics = Topic.objects.order_by('date_added')

    # The key is the variable used in the html file and value is variable usd in the view function
    context = {'topics':topics}

    return render(request, 'MainApp/topics.html', context)

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    entries = topic.entry_set.all()

    context = {'topic':topic, 'entries':entries}

    return render(request, 'MainApp/topic.html', context)

def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)

        if form.is_valid():
            form.save()

            return redirect('MainApp:topics')

    context = {'form':form} # context is a dictionary that allows use to pass data to our template. Pass form to html file
    return render(request, 'MainApp/new_topic.html', context)

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
