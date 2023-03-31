from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from bson import ObjectId
import json
from .models import *


# Create your views here.

def home(request):
    val1, val2 = templateMiddleware(request)
    products = getCars(3)

    return render(request, 'home.html',{
       "shoppingCar" : val1,
       "categories":val2,
       'products':products
    })

def product(request,product):
    try:
        val1, val2 = templateMiddleware(request)
        product = Car.objects.filter(_id=ObjectId(product)).first()
        product.id = str(product._id)
        return render(request,'product.html',{
            "shoppingCar" : val1,
            "categories":val2,
            "car": product
        })
    except Exception as e:
        raise Http404(e)


def shoppingCar(request):
    val1, val2 = templateMiddleware(request)

    car_products = val1
    total_price = 0

    for key, value in car_products.items():
        total_price += value['product']['price'] * value['quantity']

    return render(request,'myShoppingCar.html',{
        "shoppingCar" : val1,
        "categories":val2,
        "total": total_price
    })


@csrf_exempt
def addProductToCar(request):
    if request.method == 'POST':
        myShoppyCar = ShoppingCar.objects.filter(ip=request.META.get('REMOTE_ADDR') ).first()

        datos = json.loads(request.body)
        product = Car.objects.filter(_id=ObjectId(datos['product'])).first()

        serialized_car = {}
        serialized_car['_id'] = str(product._id)
        serialized_car['name'] = product.name
        serialized_car['make'] = product.make
        serialized_car['model'] = product.model
        serialized_car['year'] = product.year
        serialized_car['images'] = product.images
        serialized_car['price'] = float(str(product.price))
            

        if myShoppyCar.products == {}: 
            myShoppyCar.products = {0: {'quantity': 1, 'product': serialized_car}}
            myShoppyCar.save()
        else:
            car_products = myShoppyCar.products.copy()
            new_index = max([int(key) for key in car_products.keys()]) + 1
            car_products[str(new_index)] = {'quantity': 1, 'product': serialized_car}
            myShoppyCar.products = car_products
            myShoppyCar.save()

        return JsonResponse({'mensaje': 'Correcto', 'car': json.dumps(myShoppyCar.products,default=str) })
    else:
        return JsonResponse({'mensaje': 'Método no permitido'})


@require_GET
def searchProducts(request):
    query = request.GET.get('query')
    products = Car.objects.filter(name__icontains=query)[:4]
    data = [{'id': str(product._id), 'name': product.name, 'price': float(str(product.price)), 'images': product.images} for product in products]
    return JsonResponse(data, safe=False)




#Custom Methods
def templateMiddleware(request):
    myShoppyCar = validedShoppingCar(request.META.get('REMOTE_ADDR'))
    categories = getCategories()
    return myShoppyCar,categories

def validedShoppingCar(client_ip_address):
    shoppingCarQuery = ShoppingCar.objects.filter(ip=client_ip_address )
    try:  
        if not shoppingCarQuery.exists():
            myShoppyCar = ShoppingCar(
                ip = client_ip_address,
                products = {}
            )
            myShoppyCar.save()   
        car = myShoppyCar.products       
    except Exception as e:
        print(e)
        for shopping_car in shoppingCarQuery:
            products = shopping_car.products
            car = products 
    return car

def getCategories():
    list = {}
    categories = CarCategory.objects.all().values()
    return categories
    
def getCars(number):
    products = Car.objects.all()[:number].values()
    for product in products:
        product['id'] = product["_id"]    
    return products    