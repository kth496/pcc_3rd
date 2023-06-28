from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from learning_logs.forms import TopicForm, EntryForm
from learning_logs.models import Topic, Entry


def index(request):
    """학습 로그 홈페이지"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)  # (2)
    if topic.owner != request.user:  # (2)
        raise Http404
    entries = topic.entry_set.order_by('-date_added')  # (3)
    context = {'topic': topic, 'entries': entries}  # (4)
    return render(request, 'learning_logs/topic.html', context)  # (5)


@login_required
def new_topic(request):
    """새 주제를 추가합니다"""
    if request.method != 'POST':  # (1)
        # 데이터가 들어오지 않았으므로 빈 폼을 만듭니다
        form = TopicForm()  # (2)
    else:
        # POST 데이터를 받았으므로 이를 처리합니다
        form = TopicForm(data=request.POST)  # (3)
        if form.is_valid():
            new_topic = form.save(commit=False) # (1)
            new_topic.owner = request.user # (2)
            new_topic.save() # (3)
            return redirect('learning_logs:topics')


    # 빈 폼, 또는 유효하지 않은 폼을 표시합니다
    context = {'form': form}  # (7)
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """특정 주제에 관한 항목을 추가합니다"""
    topic = Topic.objects.get(id=topic_id)  # (1)

    if request.method != 'POST':  # (2)
        # 데이터가 들어오지 않았으므로 빈 폼을 만듭니다
        form = EntryForm()  # (3)
    else:
        # POST 데이터를 받았으므로 이를 처리합니다
        form = EntryForm(data=request.POST)  # (4)
        if form.is_valid():
            new_entry_entity = form.save(commit=False)  # (5)
            new_entry_entity.topic = topic  # (6)
            new_entry_entity.save()
            return redirect('learning_logs:topic', topic_id=topic_id)  # (7)

        # 빈 폼, 또는 유효하지 않은 폼을 표시합니다
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """기존 항목을 수정합니다"""
    entry = Entry.objects.get(id=entry_id)  # (1)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 초기 요청이므로 현재 항목으로 채운 폼을 반환합니다
        form = EntryForm(instance=entry)  # (2)
    else:
        # POST 데이터를 받았으므로 이를 처리합니다
        form = EntryForm(instance=entry, data=request.POST)  # (3)
        if form.is_valid():
            form.save()  # (4)
            return redirect('learning_logs:topic', topic_id=topic.id)  # (5)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
