import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django_filters.views import FilterView
from.models import MenuItem, Category, OrderModel
from .filters import OrderFilter

class Index(View):
    def get (self,request, *args, **kwargs):
        return render(request, 'namaste_customer/index.html')
    
class About(View):
    def get (self,request, *args, **kwargs):
        return render(request, 'namaste_customer/about.html')
    
class OrderListView(FilterView):
    model = OrderModel
    filterset_class = OrderFilter
    template_name = 'namaste_customer/order_list.html'
    context_object_name = 'filter'
           
class Order(View):
    def get (self,request, *args, **kwargs):
        # get every item from each category
        foods = MenuItem.objects.filter(category__name__contains='Foods')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')
        dessert = MenuItem.objects.filter(category__name__contains='Dessert')
        mealsets = MenuItem.objects.filter(category__name__contains='Vegetarian Meal')
        # pass into context
        context = {
            'foods' : foods,
            'drinks' : drinks,
            'dessert' : dessert,
            'mealsets' : mealsets,
        }
        # render the template
        return render(request, 'namaste_customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items ['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zipcode=zipcode
            )
        
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the customer
        body = ('Thank You for your order! Your food is being made and will be delivered soon to you! \n'
                f'Your Total: RM {price}\n'
                'Thank you again for your order!')
        
        send_mail(
            'Thank You For Your Order!',
            body,
            'namasteindia@gmail.com',
            [email],
            fail_silently=False
        )

        context = {
            'items' : order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items' : order.items,
            'price' : order.price,
        }
    
        return render(request, 'namaste_customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'namaste_customer/order_pay_confirmation.html')