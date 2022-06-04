from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
import random
import mimetypes


def home(request):
    books = Book.objects.all()
    if books:
        book1, book2, book3, book4 = random.choice(books), random.choice(books), random.choice(books), random.choice(books)
        book5, book6, book7, book8 = random.choice(books), random.choice(books), random.choice(books), random.choice(books)
        return render(request, 'main/home.html', {'book1': book1, 'book2': book2, 'book3': book3, 'book4': book4,
                                                  'book5': book5, 'book6': book6, 'book7': book7, 'book8': book8,
                                                  })
    else:
        return render(request, 'main/home.html', {})


@unauthenticated_user
def registerPage(response):
    form = RegisterForm()
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')

    return render(response, 'main/register.html', {'form': form})


@unauthenticated_user
def loginPage(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'main/login.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('/')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def user_settings(request):
    customer = request.user.customer
    customer_settings_form = CustomerSettingsForm(instance=customer)

    user = request.user
    user_settings_form = UserSettingsForm(instance=user)

    if request.method == 'POST':
        customer_settings_form = CustomerSettingsForm(request.POST, request.FILES, instance=customer)
        user_settings_form = UserSettingsForm(request.POST, instance=user)

        if customer_settings_form.is_valid():
            customer_settings_form.save()
        if user_settings_form.is_valid():
            user_settings_form.save()

            msave = Customer.objects.get(user=user)
            msave.name = request.user.username
            msave.email = request.user.email
            msave.save()

    context = {'customer_settings_form': customer_settings_form, 'user_settings_form': user_settings_form}
    return render(request, 'main/user_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def become_seller(request):
    customer = request.user.customer

    if request.method == "POST":
        customer.is_seller = True
        customer.save()
        return redirect('/book_management')

    return render(request, 'main/become_seller.html', {'customer': customer})


def user_page(request, id):
    customer = Customer.objects.get(id=id)
    books_have_all = BooksHave.objects.all()
    books_sale = customer.books_sale.split(',')[:-1]

    data_have = {}
    for i in books_have_all:
        if i.owner == customer:
            data_have[i.book.name] = i.book.id

    data_sale = {}
    for i in range(len(books_sale)):
        data_sale.update({books_sale[i]: Book.objects.get(name=books_sale[i]).id})

    context = {'customer': customer, 'data_have': data_have, 'data_sale': data_sale}
    return render(request, 'main/user_page.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def book_creation(request):
    form = BookCreationForm()
    if request.method == 'POST':
        form = BookCreationForm(request.POST, request.FILES)

        if form.is_valid():
            book_name = form.cleaned_data.get('name')
            book_author = form.cleaned_data.get('author')
            book_price = form.cleaned_data.get('price')
            book_category = form.cleaned_data.get('category')
            book_description = form.cleaned_data.get('description')
            book_picture = form.cleaned_data.get('picture')
            book_file = form.cleaned_data.get('book_file')

            if ',' in book_name:
                a = book_name.count(',')
                for i in range(a):
                    book_name = book_name.replace(',', ';')

            books = [i.name for i in Book.objects.all()]
            if book_name not in books:
                Book.objects.create(
                    seller=request.user.customer,
                    name=book_name,
                    author=book_author,
                    price=book_price,
                    category=book_category,
                    description=book_description,
                    picture=book_picture,
                    book_file=book_file,
                )
                # updating Customer.books_sale
                msave = Customer.objects.get(user=request.user)
                msave.books_sale += (book_name + ',')
                msave.save()
                return redirect('/book_management')
            else:
                form = BookCreationForm()

    return render(request, 'main/book_creation.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def book_redaction(request, id):
    book = Book.objects.get(id=id)
    form = BookRedactionForm(instance=book)
    user = book.seller.user
    old_book_name = book.name

    if request.method == 'POST':
        form = BookRedactionForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            book_name = form.cleaned_data.get('name')
            if ',' in book_name:
                a = book_name.count(',')
                for i in range(a):
                    book_name = book_name.replace(',', ';')

            form.instance.name = book_name
            form.save()

            msave = Customer.objects.get(user=user)
            bs = msave.books_sale.split(',')[:-1]
            bs[bs.index(old_book_name)] = book_name
            nbs = str()
            for i in bs:
                nbs += i + ','
            msave.books_sale = nbs
            msave.save()

            return redirect('/book_management')
    
    context = {'seller': user, 'form': form, 'pic': book.picture.url}
    return render(request, 'main/book_redaction.html', context)


def book_page(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'main/book_page.html', {'book': book})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def book_buy(request, id):
    book = Book.objects.get(id=id)
    books = BooksHave.objects.all()
    customer = request.user.customer

    dummi_flag = False
    for i in books:
        if (i.owner is customer) and (i.book is book):
            dummi_flag = True
            break

    if request.method == "POST":
        BooksHave.objects.create(
            owner=customer,
            book=book,
        )
        return redirect('/book_management')

    context = {'book': book, 'customer': customer, 'dummi_flag': dummi_flag}
    return render(request, 'main/book_buy.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def book_management(request):
    user = request.user

    books_have_all = BooksHave.objects.all()
    books_have = []
    for i in books_have_all:
        if i.owner == user.customer:
            books_have.append(i.book)

    books = Book.objects.all()
    books_sale = [book for book in books if book.seller.user == user]

    context = {'books_have': books_have, 'books_sale': books_sale}
    return render(request, 'main/book_management.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def book_delete(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        book.delete()

        msave = Customer.objects.get(user=request.user)
        bs = msave.books_sale.split(',')[:-1]
        bs.remove(book.name)
        nbs = str()
        for i in bs:
            nbs += i + ','
        msave.books_sale = nbs
        msave.save()

        return redirect('/book_management')

    context = {'book': book}
    return render(request, 'main/book_delete.html', context)


def search(request):
    books = Book.objects.all()

    searched = []
    if request.method == "POST":
        s_input = request.POST.get("search-input").lower()

        for i in books:
            if s_input in i.name.lower():
                searched.append(i)
        if  len(searched) == 0:
            for i in books:
                if s_input in i.author.lower():
                    searched.append(i)
    context = {'searched': searched}
    return render(request, 'main/search.html', context)

