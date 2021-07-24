from django.shortcuts import render, redirect
from accounts.models import Role, User
from orders.models import Order, OrderStatus, OrderType
from orders.forms import OrderWhatHappened, ReplyToCustomer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
            args['customer_orders'] = Order.objects.filter(~Q(employee=user))
            for each in args['customer_orders']:
                form = ReplyToCustomer()
                order_and_its_form[form] = each 
            args['order_and_its_form'] = order_and_its_form

            # Get list of taken orders by current employee
            choosen_orders_and_its_form = {}
            emp_orders = Order.objects.filter(employee=user)
            for each in emp_orders:
                # print(each.types.all())
                form = ReplyToCustomer()
                choosen_orders_and_its_form[form] = each
            args['choosen_orders_and_its_form'] = choosen_orders_and_its_form
        # END OF EMPLOYEE CASE

        # CUSTOMER CASE
        if user.role == 'cus':
            args['happened_form'] = OrderWhatHappened()
            args['customer_orders'] = Order.objects.filter(customer=user)
            args['customer_orders_count'] = Order.objects.count()
        # END OF CUSTOMER CASE

        return render(request, 'orders.html', args)

    if request.method == 'POST':
        data = request.POST
        # EMPLOYEE CASE
        if user.role == 'emp':
            form = ReplyToCustomer(data=data)
            print(data)
            if form.is_valid():
                # Order characteristics
                order_pk = data['order_pk']
                order_status = data['order_status']
                order_type = data['order_type']

                order = Order.objects.get(pk=order_pk)

                # Check for existent. It shoud be in the models classes, man!
                try:
                    statusObject = OrderStatus.objects.get(order_status=order_status)
                    typeObject = OrderType.objects.get(order_type=order_type)
                except:
                    statusObject = None
                    typeObject = None

                # If there are, do nothing. If there aren't, create new ones
                if not statusObject:
                    statusObject = OrderStatus.objects.create(order_status=order_status)

                if not typeObject:
                    typeObject = OrderType.objects.create(order_type=order_type)
                
                # Store these values in order row
                order.statuses.add(statusObject)
                order.types.add(typeObject)
    
                # Map employee to the order
                order.employee = user
                
                # Save it
                order.save()

                return redirect('/orders')
            else:
                args = {}
                args['errors'] = form.errors
                return render(request, 'errors.html', args)
        # END OF EMPLOYEE CASE

        # CUSTOMER CASE
        if user.role == 'cus':
            form = OrderWhatHappened(data=data)
            if form.is_valid():
                Order.objects.create(
                    customer=user, customer_telling=data['what_happened'])
                return redirect('/orders')
        # END OF CUSTOMER CASE


    return redirect('/home')
