from django.shortcuts import render, redirect
from django.contrib import messages
import sys
from WebPlantFlow.pyrebase_settings import db, auth
from WebPlantFlow.decorators import clear_session, validate_session, getSessionUser

# Create your views here.

def conta(request):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""
    return render(request,'users/conta.html', data)

def login(request):
    return render(request, 'users/login.html')


def valida_senha(request):
    email = request.POST.get('txtUserEmail', '')
    senha = request.POST.get('txtUserPassword', '')
    try:

        sign_user = auth.sign_in_with_email_and_password(email, senha)
        sign_user = auth.refresh(sign_user['refreshToken'])

        userLab = db.child("users").child(sign_user['userId']).get()

        request.session['idToken'] = sign_user['idToken']
        request.session['userEmail'] = email
        request.session['userId'] = sign_user['userId']
        request.session['nomeUsuario'] = userLab.val()['nome']
        request.session['perfilUsuario'] = userLab.val()['perfil']


    except:
        print("Entrou AQUI")
        clear_session(request)
        print(sys.exc_info()[1])
        messages.error(request, "Usuário ou senha inválidos!")
        return redirect('/usuario/entrar/')

    return redirect('/')


def sair (request):
    # for key in request.session.keys():
    # del request.session[key]
    clear_session(request)

    return render(request, "users/login.html")

def novoCadastro (request):
    data = {}
    if request.method == "POST":
        nome = request.POST.get('nome', '')
        userId = request.POST.get('userId', '')
        cidade = request.POST.get('cidade', '')
        email = request.POST.get('email', '')
        senha = request.POST.get('senha', '')

        print(nome)
        print(email)
        #print(userId)
        print(senha)

    return render(request, 'users/novoCadastro.html', data)
