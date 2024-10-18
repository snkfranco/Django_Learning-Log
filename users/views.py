from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

def logout_view(request):
    """Faz um logout od usuário conectado atualmente"""
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    """Faz o registro de novos usuários"""
    if request.method != 'POST':
        # Exibe o formulário de cadastro em branco
        form = CustomUserCreationForm()
    else:
        # Processa o formulário preenchido
        form = CustomUserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # Faz login do usuário e o redireciona para a página inicial
            login(request, new_user)  # Use 'new_user' diretamente, sem precisar autenticar novamente
            return HttpResponseRedirect(reverse('index'))
    
    # Retorna o formulário com erros (se houver) ou em branco
    context = {'form': form}
    return render(request, 'pages/register.html', context)
            