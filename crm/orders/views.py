from django.shortcuts import render, redirect
from accounts.models import Role, User
from orders.models import Order
from orders.forms import OrderWhatHappened, ReplyToCustomer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
# Create your views here.


@login_required
def orders(request):
    """
    Returns specific page for customer and for employee
    """
    user = request.user

    args = {}

    if request.method == 'GET':
        args['role'] = user.role
        args['username'] = user.username

        # EMPLOYEE CASE
        if user.role == 'emp':
            order_and_its_form = {}
            args['customer_orders'] = Order.objects.all()
            for each in args['customer_orders']:
                form = ReplyToCustomer()
                order_and_its_form[form] = each 
            args['order_and_its_form'] = order_and_its_form

            choosen_orders_and_its_form = {}
            emp_orders = Order.objects.filter(employee=user)
            for each in emp_orders:
                form = ReplyToCustomer()
                choosen_orders_and_its_form[form] = each
            args['choosen_orders_and_its_form'] = choosen_orders_and_its_form

        # CUSTOMER CASE
        if user.role == 'cus':
            args['happened_form'] = OrderWhatHappened()
            args['customer_orders'] = Order.objects.filter(customer=user)
            args['customer_orders_count'] = Order.objects.count()

        return render(request, 'orders.html', args)

    if request.method == 'POST':
        data = request.POST
        if user.role == 'cus':
            form = OrderWhatHappened(data=data)
            if form.is_valid():
                Order.objects.create(
                    customer=user, customer_telling=data['what_happened'])
                return redirect('/orders')

    return redirect('/home')
