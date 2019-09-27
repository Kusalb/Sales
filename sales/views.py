from django.contrib import auth, messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from sales.forms import CustomUserCreationForm, ShopForm, EmployeeForm, CustomerForm, ProductForm, DealForm
from sales.models import Employee, Customer, Product, Deals

from django.views import generic

from sales.models import Shop, CustomUser
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Shop
from .serializers import shopSerializer, customerSerializer, productSerializer


class shopList(APIView):

    def get(self, request):
        shop = Shop.objects.all()
        serialzer = shopSerializer(shop, many=True)
        return Response(serialzer.data)

    def post(self):
        pass


class customerList(APIView):
    def get(self, request):
        customer = Customer.objects.all()
        serialzer = customerSerializer(customer, many=True)
        return Response(serialzer.data)

    def post(self):
        pass


class productList(APIView):
    def get(self, request):
        product = Product.objects.all()
        serialzer = productSerializer(product, many=True)
        return Response(serialzer.data)

    def post(self):
        pass


def login(request):
    return render(request, 'login/login.html')


# Sign up class
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def log(request):
    return render(request, 'login/login.html')


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                if user.is_admin:
                    return redirect('admin_dash')
                elif user.is_customer:
                    return redirect('customer_dash')
                elif user.is_shop:
                    return redirect('shop_dash')

            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'login/login.html')

        except auth.ObjectDoesNotExist:
            print("invalid user")

    return render(request, 'login/login.html')


def admin_dash(request):
    return render(request, 'admin/admin_dashboard.html')


def customer_dash(request):
    return render(request, 'customer/customer_dashboard.html')


def shop_dash(request):
    return render(request, 'shop/shop_dashboard.html')


def shop_sign(request):
    return render(request, 'shop/shop_sign_up.html')


def customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                email = request.POST.get('email')
                password1 = request.POST.get("password")
                print(password1)
                customer = form.save()
                use = CustomUser.objects.create(username=email, is_customer=True)
                use.set_password(password1)
                use.save()
                idi = use.id
                print(idi)
                customer.CustomUser_id = CustomUser.objects.get(id=idi)
                customer.save()
                return redirect('/customershow')
            except:
                pass
    else:
        form = CustomerForm()
    return render(request, 'customer/customer_new.html', {'form': form})


def customershow(request):
    customer = Customer.objects.all()
    return render(request, "customer/customer_list.html", {'customer': customer})


def customeredit(request, id):
    customer = Customer.objects.get(id=id)
    return render(request, 'customer/customer_edit.html', {'customer': customer})


def customerupdate(request, id):
    customer = Customer.objects.get(id=id)
    form = CustomerForm(request.POST, request.FILES or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect("/customershow")
    return render(request, 'customer/customer_edit.html', {'customer': customer})


def customerdestroy(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect("/customershow")


def shop(request):
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES or None)
        if form.is_valid():
            print(form)
            try:
                email = request.POST.get('email')
                password1 = request.POST.get("password")
                print(password1)
                shop = form.save()
                use = CustomUser.objects.create(username=email, is_shop=True)
                use.set_password(password1)
                use.save()
                idi = use.id
                print(idi)
                shop.CustomUser_id = CustomUser.objects.get(id=idi)
                shop.save()
                return redirect('/login')
            except:
                pass
    else:
        form = ShopForm()
    return render(request, 'shop/shop_new.html', {'form': form})


def shopshow(request):
    shop = Shop.objects.all()
    return render(request, 'shop/shop_list.html', {'shop': shop})


def shopedit(request, id):
    shop = Shop.objects.get(id=id)
    return render(request, 'shop/shop_edit.html', {'shop': shop})


def shopupdate(request, id):
    shop = Shop.objects.get(id=id)
    form = ShopForm(request.POST, request.FILES or None, instance=shop, )
    if form.is_valid():
        form.save()
        return redirect("/shopshow")
    return render(request, 'shop/shop_edit.html', {'shop': shop})


def shopdestroy(request, id):
    shop = Shop.objects.get(id=id)
    shop.delete()
    return redirect('/shopshow')


def product(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES or None)
        if form.is_valid():
            try:
                form.save()
                return redirect('/productshow')
            except:
                pass
    else:
        form = ProductForm()
    return render(request, 'product/product_new.html', {'form': form})


def productshow(request):
    product = Product.objects.all()
    return render(request, 'product/product_list.html', {'product': product})


def productedit(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product/product_edit.html', {'product': product})


def productupdate(request, id):
    product = Product.objects.get(id=id)
    print(product)
    form = ProductForm(request.POST,request.FILES or None, instance=product)
    print(form)
    if form.is_valid():
        print('1')
        form.save()
        return redirect('/productshow')
    print('2')
    return render(request, 'product/product_edit.html', {'product': product})


def productdestroy(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('/productshow')


def deal(request):
    if request.method == "POST":
        form = DealForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                form.save()
                return redirect('/dealshow')
            except:
                pass
    else:
        form = DealForm()
    return render(request, 'deal/deal_new.html', {'form': form})


def dealshow(request):
    deal = Deals.objects.all()
    return render(request, 'deal/deal_list.html', {'deal':deal})

def dealedit(request, id):
    deal = Deals.objects.get(id = id)
    return render(request, 'deal/deal_edit.html', {'deal': deal})

def logout(request):
    auth.logout(request)
    return render(request, 'login/login.html')


def dealupdate(request,id):
    deal = Deals.objects.get(id=id)
    form = DealForm(request.POST, request.FILES or None, instance=deal )
    if form.is_valid():
        form.save()
        return redirect('/dealshow')
    return render(request, 'deal/deal_edit.html', {'deal': deal})


def dealdestroy(request, id):
    deal = Deals.objects.get(id=id)
    deal.delete()
    return redirect('/dealshow')


def index(request):
    return render(request, 'login/index.html')