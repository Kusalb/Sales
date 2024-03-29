from django.contrib import auth, messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from sales.forms import CustomUserCreationForm, ShopForm, CustomerForm, ProductForm, DealForm, SearchForm, \
    AdvertisementForm
from sales.models import Customer, Product, Deals, Advertisement

from django.views import generic

from sales.models import Shop, CustomUser
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
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
                return redirect('login')
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
        form = ProductForm(request.POST, request.FILES or None)
        print(form)
        if form.is_valid():
            try:
                product = form.save()
                use = request.user.id
                print(use)
                product.Shop_id = Shop.objects.get(CustomUser_id=use)
                print(product.Shop_id)
                product.CustomUser_id = CustomUser.objects.get(id=use)
                print(product.CustomUser_id)
                product.save()
                return redirect('/productshow')
            except:
                pass
    else:
        form = ProductForm()
    return render(request, 'product/product_new.html', {'form': form})


def productshow(request):
    use = request.user.id
    if request.user.is_shop:
        product = Product.objects.filter(CustomUser_id=use)
    if request.user.is_admin:
        product = Product.objects.all()
    return render(request, 'product/product_list.html', {'product': product})


def productedit(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product/product_edit.html', {'product': product})


def productupdate(request, id):
    product = Product.objects.get(id=id)
    print(product)
    form = ProductForm(request.POST, request.FILES or None, instance=product)
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
                deal = form.save()
                use = request.user.id
                deal.CustomUser_id = CustomUser.objects.get(id=use)
                deal.Shop_id = Shop.objects.get(CustomUser_id=use)
                deal.save()
                return redirect('/dealshow')
            except:
                pass
    else:
        form = DealForm()
    return render(request, 'deal/deal_new.html', {'form': form})


def dealshow(request):
    use = request.user.id
    id = str(use)
    if request.user.is_shop:
        deal = Deals.objects.filter(CustomUser_id=id)
    if request.user.is_admin:
        deal = Deals.objects.filter()
    return render(request, 'deal/deal_list.html', {'deal': deal})


def dealedit(request, id):
    deal = Deals.objects.get(id=id)
    return render(request, 'deal/deal_edit.html', {'deal': deal})


def logout(request):
    auth.logout(request)
    return render(request, 'login/login.html')


def dealupdate(request, id):
    deal = Deals.objects.get(id=id)
    form = DealForm(request.POST, request.FILES or None, instance=deal)
    if form.is_valid():
        form.save()
        return redirect('/dealshow')
    return render(request, 'deal/deal_edit.html', {'deal': deal})


def dealdestroy(request, id):
    deal = Deals.objects.get(id=id)
    deal.delete()
    return redirect('/dealshow')


def index(request):
    deal = Deals.objects.filter(is_approve=True)
    shop = Shop.objects.all()
    advertisement = Advertisement.objects.all()
    context = {
        'deal': deal,
        'advertisement': advertisement
    }

    return render(request, 'login/index.html', context)


def approve_deal(request, id):
    status = request.POST.get('status')
    deal = Deals.objects.get(pk=id)
    flag = False
    if status == 'true':
        flag = True
    deal.is_approve = flag
    deal.save()
    return JsonResponse({'status': flag})


def approve_product(request, id):
    status = request.POST.get('status')
    product = Product.objects.get(pk=id)
    flag = False
    if status == 'true':
        flag = True
    product.is_approve = flag
    product.save()
    return JsonResponse({'status': flag})


def find(request):
    location = request.POST.get('location')
    category = request.POST.get('category')
    try:
        if category == 'Clothes':
            result = Shop.objects.filter(category='Clothes', location=location)
            result_count = Shop.objects.filter(category='Clothes', location=location).count()

        elif category == 'Shoes':
            result = Shop.objects.filter(category='Shoes', location=location)
            result_count = Shop.objects.filter(category='Shoes', location=location).count()

        elif category == 'Electronics':
            result = Shop.objects.filter(category='Electronics', location=location)
            result_count = Shop.objects.filter(category='Electronics', location=location).count()

        elif category == 'Automobile':
            result = Shop.objects.filter(category='Automobile', location=location)
            result_count = Shop.objects.filter(category='Automobile', location=location).count()
        elif category == 'Makeup':
            result = Shop.objects.filter(category='Makeup', location=location)
            result_count = Shop.objects.filter(category='Makeup', location=location).count()
        elif category == 'Shoes':
            result = Shop.objects.filter(category='Shoes', location=location)
            result_count = Shop.objects.filter(category='Shoes', location=location).count()

        offer_result = Deals.objects.filter(is_approve=True, Shop__location=location)
        context = {
            'item': result,
            'offer_result': offer_result,
            'result_count': result_count
        }
    except:
        return redirect('index')

    print(context)
    return render(request, 'login/find.html', context )


def shop_info(request, id):
    deal = Deals.objects.get(id=id)
    shop = Shop.objects.get(id=deal.Shop_id)
    context = {
        'deal': deal,
        'shop': shop
    }
    return render(request, 'shop/shop_info.html', context)


def advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                form.save()
                return redirect('advertisementshow')
            except:
                pass
    else:
        form = AdvertisementForm()
    return render(request, 'advertisement/advertisement_new.html', {'form': form})


def advertisementshow(request):
    advertisement = Advertisement.objects.all()
    return render(request, 'advertisement/advertisement_list.html', {'advertisement': advertisement})


def advertisementedit(request, id):
    advertisement = Advertisement.objects.get(id=id)
    return render(request, 'advertisement/advertisement_edit.html', {'advertisement': advertisement})


def advertisementupdate(request, id):
    advertisement = Advertisement.objects.get(id=id)
    form = AdvertisementForm(request.POST, request.FILES or None, instance=advertisement)
    if form.is_valid():
        form.save()
        return redirect('/advertisementshow')
    return render(request, 'advertisement/advertisement_edit.html', {'advertisement': advertisement})


def advertisementdestroy(request, id):
    advertisement = Advertisement.objects.get(id=id)
    advertisement.delete()
    return redirect('/advertisementshow')


def cat_clothes(request):
    clothes = Deals.objects.filter(Shop__category='clothes', is_approve=True)
    return render(request, 'category/clothes.html', {'cat_clothes': clothes})


def cat_shoes(request):
    shoes = Deals.objects.filter(Shop__category='shoes', is_approve=True)
    return render(request, 'category/shoes.html', {'cat_shoes': shoes})


def cat_automobile(request):
    automobile = Deals.objects.filter(Shop__category='automobile', is_approve=True)
    return render(request, 'category/automobile.html', {'cat_automobile': automobile})


def cat_makeup(request):
    makeup = Deals.objects.filter(Shop__category='makeup', is_approve=True)
    return render(request, 'category/makeup.html', {'cat_makeup': makeup})


def cat_electronics(request):
    electronics = Deals.objects.filter(Shop__category='electronics', is_approve=True)
    return render(request, 'category/electronics.html', {'cat_electronics': electronics})
