from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from django.views import View

# Create your views here.

class Order_Create(View):
    """
        creation d'ordre d'achat
    """
    
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart,
                                                            'form': form})
        
    
    def post(self, request):
        cart = Cart(request)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                    
                # effacer le panier
                cart.clear()
                # launch asynchranous task
                order_created.delay(order.id)
              
                return render(request, 'orders/order/created.html', {'order': order})
            


