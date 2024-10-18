from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    """Página principal do Learning_Log"""
    return render(request, 'pages/index.html')

@login_required
def topics(request):
    """Mostra todos os tópicos"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'pages/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas."""
    topic = Topic.objects.get(id=topic_id)
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}  # Passa topic_id
    return render(request, 'pages/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona um novo tópico"""
    if request.method != 'POST':
        # Nenhum dado submetido. cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos, processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form': form}
    return render(request, 'pages/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adiciona uma nova anotação para um assunto particular"""
    topic = Topic.objects.get(id = topic_id)
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Nenhum dado submetido, cria um formulário em branco
        form = EntryForm()
        
    else:
        # Dados submetidos, processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    
    context = {'topic':topic, 'form':form}
    return render(request, 'pages/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
       # Nenhum dado foi submetido, ele apenas preenche a entrada com o formulário atual
        form = EntryForm(instance=entry)
    else:
        # Dados de POST submetidos, portanto, processa as alterações
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
        
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'pages/edit_entry.html', context)
        
        
        
        
        
        
        
        
        
        
        