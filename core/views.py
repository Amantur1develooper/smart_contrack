from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправляем пользователя на страницу после входа
            return redirect('main')
        else:
            # Обработка неверных учетных данных
            return redirect('login')
    else:
        # Обработка GET запроса, например, отображение формы входа
        return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def register1(request):

    return render(request, 'perehod.html')

def register2(request):
    form = UserForm()
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('valid')
            return redirect('/main/')  
        
    return render(request, 'register.html', {'form': form,})

def blockchain_view(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            # Обработка данных формы
            buyer = form.cleaned_data['buyer']
            seller = form.cleaned_data['seller']
            item = form.cleaned_data['item']
            price = form.cleaned_data['price']
            payment_terms = form.cleaned_data['payment_terms']
            delivery_terms = form.cleaned_data['delivery_terms']
            warranty = form.cleaned_data['warranty']
            dispute_resolution = form.cleaned_data['dispute_resolution']
            podpis1 = form.cleaned_data['podpis1']
            podpis2 = form.cleaned_data['podpis2']
            print(podpis1,'-----------------------------')
            previous_block = Contract.objects.last()
            if previous_block:
                index = previous_block.index + 1
                previous_hash = previous_block.hash
            else:
                index = 0
                previous_hash = '0'
        
            new_block = Contract(index=index, buyer=buyer, seller=seller, price=price, item=item, payment_terms=payment_terms,
                             delivery_terms=delivery_terms, dispute_resolution=dispute_resolution, podpis1=podpis1, podpis2=podpis2, warranty=warranty, previous_hash=previous_hash)
            new_block.save()
            return redirect('main')
    else:
        form = ContractForm()
    
    blocks = Contract.objects.all()
    return render(request, 'dogovor1.html', {'blocks': blocks, 'form': form})

def alldogovor(request):
    blocks = Contract.objects.all()
    corruption_detected = check_blockchain_integrity(blocks)
    if corruption_detected:
        messages.error(request, 'Коррупция данных обнаружена!{}'.format(corruption_detected))
        cor_block = []
        for item in corruption_detected:
            cor_block.append(blocks.get(index=item))
            blocks = blocks.exclude(index=item)
        print(cor_block)
        return render(request,'all_dogovor.html',{'blocks':blocks, 'cor_block':cor_block} )
    return render(request,'all_dogovor.html',{'blocks':blocks, } )


def check_blockchain_integrity(blocks):
    lst = []
    for i in range(1, len(blocks)):
        current_block = blocks[i]
        previous_block = blocks[i - 1]
        
        if current_block.previous_hash != previous_block.hash:
            lst.append(previous_block.index)
    return lst  # Коррупция обнаружена
        

    return False
# def dogovor1(request):
#     form = ContractForm()
#     if request.method == 'POST':
#         form = ContractForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/main/') 
#     return render(request, 'dogovor1.html', {'form': form})

def dogovor(request):
    return render(request, 'dogovor.html')

def q_answer(request):
    return render(request, 'q_answer.html')


def about_us(request):
    return render(request, 'about_us.html')

def logout_view(request):
    logout(request)
    return redirect('main')
