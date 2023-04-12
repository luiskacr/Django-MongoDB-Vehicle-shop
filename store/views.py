from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId
from .models import *
from datetime import date
import json


# Create your views here.
def home(request):
    val1, val2 = templateMiddleware(request)
    products = getCars(3)

    return render(request, 'home.html', {
        "shoppingCar": val1,
        "categories": val2,
        'products': products
    })


def category(request, name):
    val1, val2 = templateMiddleware(request)
    db = mongoConeccion('store_car')
    products = list(db.aggregate([
        {
            '$match': {
                "category.name": name
            }
        }
    ]))

    for product in products:
        product["_id"] = str(product["_id"] )

    return render(request, 'category.html',{
        "shoppingCar": val1,
        "categories": val2,
        'products': products,
        'category': name
    })


def product(request, product_ID):
    try:
        val1, val2 = templateMiddleware(request)
        product = Car.objects.filter(_id=ObjectId(product_ID)).first()
        product.id = str(product._id)
        return render(request, 'product.html', {
            "shoppingCar": val1,
            "categories": val2,
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

    return render(request, 'myShoppingCar.html', {
        "shoppingCar": val1,
        "categories": val2,
        "total": total_price
    })


def checkout(request):
    val1, val2 = templateMiddleware(request)

    car_products = val1
    total_price = 0

    for key, value in car_products.items():
        total_price += value['product']['price'] * value['quantity']

    return render(request, 'checkout.html', {
        "shoppingCar": val1,
        "categories": val2,
        "total": total_price,
    })


@csrf_exempt
def payment(request):
    if request.method == 'POST':
        try:
            db = mongoConeccion('store_order')
            data = json.loads(request.body)

            if data["promo"] != '':
                promo = PromoCode.objects.filter(_id=ObjectId(data['promo']['_id'])).first()
                promo.discount = float(promo.discount.to_decimal())
                promo.quantity = promo.quantity - 1
                promo.save()

            shoppingCar = ShoppingCar.objects.filter(ip=request.META.get('REMOTE_ADDR')).first()
            shoppingCar.delete()

            data_dict = json.loads(json.dumps(data, default=str))
            data_dict['_id'] = ObjectId()
            data_dict['date'] = str(date.today())
            newOrder = db.insert_one(data_dict)

            return JsonResponse({'code': 200, 'orden': str(newOrder.inserted_id)})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': e})
    else:
        return JsonResponse({'code': 404, 'mensaje': 'Método no permitido'})


def thanks(request, order):
    val1, val2 = templateMiddleware(request)

    db = mongoConeccion('store_order')
    order = db.find_one({"_id": ObjectId(order)})
    order["id"] = str(order["_id"])

    return render(request, 'thanks.html', {
        "shoppingCar": val1,
        "categories": val2,
        'order': order
    })


@csrf_exempt
def redeemPromoCode(request):
    if request.method == 'POST':
        clientCode = json.loads(request.body)
        clientCode = clientCode['code']

        promoCode = PromoCode.objects.filter(code=clientCode).first()

        if promoCode == None:
            return JsonResponse({'code': 400, 'mensaje': 'Codigo No existe'})

        promo = {'_id': str(promoCode._id), 'code': promoCode.code, 'discount': float(str(promoCode.discount))}

        return JsonResponse({'code': 200, 'promo': promo})
    else:
        return JsonResponse({'code': 404, 'mensaje': 'Método no permitido'})


@csrf_exempt
def addProductToCar(request):
    if request.method == 'POST':
        myShoppyCar = ShoppingCar.objects.filter(ip=request.META.get('REMOTE_ADDR')).first()

        datos = json.loads(request.body)
        product = Car.objects.filter(_id=ObjectId(datos['product'])).first()

        serialized_car = {'_id': str(product._id), 'name': product.name, 'make': product.make, 'model': product.model,
                          'year': product.year, 'images': product.images, 'price': float(str(product.price))}

        if myShoppyCar.products == {}:
            myShoppyCar.products = {0: {'quantity': 1, 'product': serialized_car}}
            myShoppyCar.save()
        else:
            car_products = myShoppyCar.products.copy()
            new_index = max([int(key) for key in car_products.keys()]) + 1
            car_products[str(new_index)] = {'quantity': 1, 'product': serialized_car}
            myShoppyCar.products = car_products
            myShoppyCar.save()

        return JsonResponse({'mensaje': 'Correcto', 'car': json.dumps(myShoppyCar.products, default=str)})
    else:
        return JsonResponse({'mensaje': 'Método no permitido'})


@require_GET
def searchProducts(request):
    query = request.GET.get('query')
    products = Car.objects.filter(name__icontains=query)[:4]
    data = [{'id': str(product._id), 'name': product.name, 'price': float(str(product.price)), 'images': product.images}
            for product in products]
    return JsonResponse(data, safe=False)


def templateMiddleware(request):
    myShoppyCar = validedShoppingCar(request.META.get('REMOTE_ADDR'))
    categories = getCategories()
    return myShoppyCar, categories


def validedShoppingCar(client_ip_address):
    shoppingCarQuery = ShoppingCar.objects.filter(ip=client_ip_address)
    try:
        if not shoppingCarQuery.exists():
            myShoppyCar = ShoppingCar(
                ip=client_ip_address,
                products={}
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


def mongoConeccion(document):
    CLIENT = settings.DATABASES['default']['CLIENT']
    NAME = settings.DATABASES['default']['NAME']
    client = MongoClient(CLIENT['host'],
                         username=CLIENT['username'],
                         password=CLIENT['password'],
                         )
    db = client[NAME]
    return db[document]
