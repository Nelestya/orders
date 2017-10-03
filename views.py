from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .models import OrderItem, Order
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from django.views import View
from baseapp.models import Application
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

# Create your views here.

class Order_Create(View):
    """
        creation d'ordre d'achat
    """

    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        applications = Application.objects.all()
        return render(request, 'orders/order/create.html', {'cart': cart,
                                                            'applications': applications,
                                                            'form': form})


    def post(self, request):
        cart = Cart(request)
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
            # set the order in the sessions
            request.session['order_id'] = order.id
            # redirect payment
            return redirect(reverse('payment:process'))


class Admin_Order_Detail(View):
        @staff_member_required
        def get(self, request, order_id):
            order = get_object_or_404(Order, id=order_id)
            return render(request, 'admin/orders/order/detail.html')

        @staff_member_required
        def post(self, request):
            pass
