import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_log.settings")

import django
django.setup()

from MainApp.models import Topic, Entry
#NoSQL coding
topics = Topic.objects.all()

for topic in topics:
    print(topic.id)
    print(topic) #topic.text returns same thing
    print(topic.date_added)


t = Topic.objects.get(id=1)
print(t) #Chess

entries = t.entry_set.all()

for e in entries:
    print(e)
