from django.shortcuts import render, redirect
from accounts.models import Role, User
from orders.models import Order, OrderStatus, OrderType
from orders.forms import OrderWhatHappened, ReplyToCustomer, NewCustomerNewOrder
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
        args['user'] = user

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
        if not 'change_order' in data:
            redirect('/order')
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


                # Check if these type and status exists. If not, then create.
                if not order_status:    # if post string is empty use old status
                    order_status = order.order_status
                else:
                    orderStatus = OrderStatus.objects.filter(order_status=order_status)
                    print(orderStatus)
                    if not orderStatus.exists():
                        order_status = OrderStatus.objects.create(order_status=order_status)
                    else:
                        order_status = orderStatus.first()


                if not order_type:      # if post string is empty use old type
                    order_type = order.order_type
                else:
                    orderType = OrderType.objects.filter(order_type=order_type)
                    if not orderType.exists():
                        order_type = OrderType.objects.create(order_type=order_type)
                    else:
                        order_type = orderType.first()

                # finally mapping type and status with order
                order.order_status = order_status
                order.order_type = order_type

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
            print(data)
            if form.is_valid():
                orderStatus = OrderStatus.objects.filter(order_status='Open')
                orderType = OrderType.objects.filter(order_type='UnderReview')
                if(orderStatus.count() == 0):
                    orderStatus = OrderStatus.objects.create(order_status='Open')
                else:
                    orderStatus = orderStatus.first()

                if(orderType.count() == 0):
                    orderType = OrderType.objects.create(order_type='UnderReview')
                else:
                    orderType = orderType.first()

                Order.objects.create(
                    customer=user, customer_telling=data['what_happened'], order_status=orderStatus, order_type=orderType)
                return redirect('/orders')
        # END OF CUSTOMER CASE
    return redirect('/home')

@login_required
def delete_order(request, ID):
    if request.method == 'GET':
        order = Order.objects.get(pk=ID)
        if order.customer == request.user:
            order.delete()
            return redirect('/orders')
        else:
            return HttpResponse('You don\'t have permission to do this!')
    else:
        return redirect('/orders')

@login_required
def leave_order(request, ID):
    pass

@login_required
def create_customer_create_order(request):
    if request.method == 'POST':
        data = request.POST
        if not 'phone_customer' in data:
            pass
        else:
            # create customer and map order to him and also map yourself to the order
            pass
        return HttpResponse('create_customer_create_order')