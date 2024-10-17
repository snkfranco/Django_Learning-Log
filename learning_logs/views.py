from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    """Página principal do Learning_Log"""
    return render(request, 'pages/index.html')

def topics(request):
    """Mostra todos os tópicos"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'pages/topics.html', context)

def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}  # Passa topic_id
    return render(request, 'pages/topic.html', context)

def new_topic(request):
    """Adiciona um novo tópico"""
    if request.method != 'POST':
        # Nenhum dado submetido. cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos, processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form': form}
    return render(request, 'pages/new_topic.html', context)

def new_entry(request, topic_id):
    """Adiciona uma nova anotação para um assunto particular"""
    topic = Topic.objects.get(id = topic_id)
    
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
    
def edit_entry(request, entry_id):
    """Edita uma entrada existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
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
        
        
        
        
        
        
        
        
        
        
        